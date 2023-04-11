#  Copyright (c) 2023, plun1331
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import asyncio
from io import BytesIO
import logging
import time
import zlib
from typing import TYPE_CHECKING

from cryptography.hazmat.primitives.ciphers import Cipher, CipherContext

from minecraft.packets.login_serverbound import EncryptionResponse
from .dispatcher import Dispatcher
from .reactors import REACTORS
from .reactors.base import REACTOR
from ..datatypes import *
from ..enums import NextState, State
from ..exceptions import MalformedPacketSizeError, PacketParsingError
from ..packets import (
    get_packet,
    Handshake,
    LoginStart,
    PACKET,
)

if TYPE_CHECKING:
    from ..client import Client

log = logging.getLogger(__name__)

PROTOCOL_VERSION: int = 762
RELEASE_NAME: str = "1.19.4"


class Connection:
    """
    Handles sending and recieving packets from the server.

    :ivar client: The client that this connection is attached to.
    :vartype client: Client
    :ivar host: The host that the connection is connected to.
    :vartype host: str
    :ivar port: The port that the connection is on.
    :vartype port: int
    :ivar state: The current state of the connection.
    :vartype state: State
    :ivar closed: Whether or not the connection has been closed.
    :vartype closed: bool
    :ivar loop: The event loop that the connection is running on.
    :vartype loop: asyncio.AbstractEventLoop
    :ivar reader: The reader that the connection is using to read packets.
    :vartype reader: asyncio.StreamReader
    :ivar writer: The writer that the connection is using to write packets.
    :vartype writer: asyncio.StreamWriter
    :ivar outgoing_packets: The queue of packets that are waiting to be sent.
    :vartype outgoing_packets: asyncio.Queue
    :ivar dispatcher: The dispatcher that is handling incoming packets.
    :vartype dispatcher: Dispatcher
    :ivar using_compression: Whether or not the connection is using compression.
    :vartype using_compression: bool
    :ivar use_encryption: Whether or not the connection is using encryption.
    :vartype use_encryption: bool
    :ivar shared_secret: The shared secret that is being used for encryption.
    :vartype shared_secret: bytes
    :ivar cipher: The cipher that is being used for encryption.
    :vartype cipher: cryptography.hazmat.primitives.ciphers.Cipher
    :ivar reactor: The reactor that is currently handling packets.
    :vartype reactor: Reactor
    """

    def __init__(self, client):
        self.client: Client = client
        self.host: str | None = None
        self.port: int | None = None
        self.state: State = State.HANDSHAKE
        self.closed: bool = False

        self.loop: asyncio.AbstractEventLoop | None = None
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.outgoing_packets: asyncio.Queue[PACKET] = asyncio.Queue()
        self.dispatcher: Dispatcher = Dispatcher(self)
        self.reactor: REACTOR | None = None

        self.use_encryption: bool = False
        self.shared_secret: bytes | None = None
        self.cipher: Cipher | None = None
        self.encryptor: CipherContext | None = None
        self.decryptor: CipherContext | None = None

        self.use_compression: bool = False
        self.compression_threshold: int = 0

        self._running: asyncio.Future | None = None
        self._read_task: asyncio.Task | None = None
        self._write_task: asyncio.Task | None = None

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypts the given data using the connection's cipher.

        :params data: The data to encrypt.
        :type data: bytes

        :return: The encrypted data.
        :rtype: bytes
        """
        if not self.use_encryption:
            return data
        if self.encryptor is None:
            raise RuntimeError("Cannot encrypt without an encryptor")
        return self.encryptor.update(data)

    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypts the given data using the connection's cipher.

        :params data: The data to decrypt.
        :type data: bytes

        :return: The decrypted data.
        :rtype: bytes
        """
        if not self.use_encryption:
            return data
        if self.decryptor is None:
            raise RuntimeError("Cannot decrypt without a decryptor")
        return self.decryptor.update(data)

    def compress(self, data: bytes) -> tuple[bytes, bool]:
        """
        Compresses the given data, if necessary.

        :params data: The data to compress.
        :type data: bytes

        :return: The compressed data, as well as a boolean indicating
                 whether or not the data was actually compressed.
        :rtype: tuple[bytes, bool]
        """
        if not self.use_compression:
            return data, False
        if len(data) < self.compression_threshold:
            return data, False
        return zlib.compress(data), True

    def decompress(self, data: bytes) -> bytes:
        """
        Decompresses the given data, if compression is enabled.

        :params data: The data to decompress.
        :type data: bytes

        :return: The decompressed data.
        :rtype: bytes
        """
        if not self.use_compression:
            return data
        return zlib.decompress(data)

    async def connect(self, host: str, port: int) -> None:
        """
        Connects to the given host and port.

        :params host: The host to connect to.
        :type host: str
        :params port: The port to connect to.
        :type port: int
        """
        log.info(
            f"Connecting to %s:%s with protocol version {PROTOCOL_VERSION} ({RELEASE_NAME})",
            host,
            port,
        )
        self.host = host
        self.port = port
        self.loop = asyncio.get_running_loop()
        self._running = asyncio.Future()
        self.reader, self.writer = await asyncio.open_connection(host, port)
        self._read_task = self.loop.create_task(self._read_loop())
        self._write_task = self.loop.create_task(self._write_loop())
        log.info("Started read/write tasks")

    async def parse_varint(self) -> int:
        value = 0
        position = 0
        while True:
            read = await self.reader.read(1)
            if read == b"":
                await asyncio.sleep(0.01)
                continue
            read = self.decrypt(read)
            current_byte = read[0]
            value |= (current_byte & 0x7F) << position
            if (current_byte & 0x80) == 0:
                break
            position += 7
            if position >= 32:
                raise ValueError("VarInt is too big")
        return value

    async def _read_loop(self) -> None:
        try:
            while True:
                packet_length = await self.parse_varint()
                log.debug("Reader < Recieving packet of length %s", packet_length)
                if packet_length > 2097151:
                    log.error(
                        "Reader x< Packet length %s is too large, terminating connection",
                        packet_length,
                    )
                    await self.close(
                        error=MalformedPacketSizeError(
                            f"Packet length of {packet_length} is too large"
                        )
                    )
                    return

                packet_data = self.decrypt(await self.reader.readexactly(packet_length))
                if len(packet_data) != packet_length:
                    log.error(
                        "Reader x< Packet length %s does not match "
                        "expected length %s, terminating connection",
                        len(packet_data),
                        packet_length,
                    )
                    await self.close(
                        error=MalformedPacketSizeError(
                            f"Packet length of {len(packet_data)} did not match expected length of {packet_length}"
                        )
                    )
                    return

                buffer = BytesIO(packet_data)

                data_length = 0
                if self.use_compression:
                    data_length = Varint.from_bytes(buffer).value
                    log.debug(
                        "Reader < Recieving packet of decompressed length %s",
                        data_length,
                    )
                    packet_data = buffer.read()
                if data_length > 2097151:
                    log.error(
                        "Reader x< Packet length %s is too large, terminating connection",
                        data_length,
                    )
                    await self.close(
                        error=MalformedPacketSizeError(
                            f"Packet length of {data_length} is too large"
                        )
                    )
                    return
                if data_length > 0:
                    packet_data = self.decompress(packet_data)
                    if len(packet_data) != data_length:
                        log.error(
                            "Reader x< Packet length %s does not match "
                            "expected uncompressed length %s, terminating connection",
                            len(packet_data),
                            data_length,
                        )
                        await self.close(
                            error=MalformedPacketSizeError(
                                f"Packet length of {len(packet_data)} did not match expected length of {data_length}",
                            )
                        )
                        return
                try:
                    packet = get_packet(packet_data, state=self.state)
                except PacketParsingError as exc:
                    log.exception(
                        "Reader < Failed to parse packet with id %s",
                        Varint.from_bytes(BytesIO(packet_data)).value,
                        exc_info=exc,
                    )
                    continue

                log.debug("Reader < Recieved %s", packet.__class__.__name__)
                if self.reactor and packet.__class__ in self.reactor.handlers:
                    log.debug(
                        "Dispatching %s to reactor handler",
                        packet.__class__.__name__
                    )
                    await self.reactor.handlers[packet.__class__](packet)
                self.dispatcher.dispatch(packet)
        except asyncio.CancelledError:
            log.error("Reader : Read loop cancelled")
        except Exception:  # pylint: disable=broad-except
            log.exception("Reader : Error in read loop")
            await self.close()

    async def _write_loop(self) -> None:
        try:
            while True:
                packet: PACKET = await self.outgoing_packets.get()
                if packet.state != self.state:
                    log.error(
                        "Writer x> Illegal packet %s " " during %s (expected state %s)",
                        packet.__class__.__name__,
                        self.state.name,
                        packet.state.name,
                    )
                    continue
                if isinstance(packet, Handshake):
                    self.change_state(State.from_value(packet.next_state.value))

                log.debug(
                    "Writer > Sending %s (%s)",
                    packet.__class__.__name__,
                    packet.packet_id,
                )
                packet_length = len(packet)
                if packet_length > 2097151:
                    log.error(
                        f"Writer x> Packet length {packet_length} is too large, terminating connection"
                    )
                    await self.close(
                        error=MalformedPacketSizeError(
                            f"Packet length of {packet_length} is too large"
                        )
                    )
                    return

                packet_data, was_compressed = self.compress(bytes(packet))
                if self.use_compression:
                    data_length = packet_length if was_compressed else 0
                    packet_length = len(packet_data)
                    packet_data = (
                        bytes(Varint(packet_length))
                        + bytes(Varint(data_length))
                        + packet_data
                    )
                else:
                    packet_data = bytes(Varint(packet_length)) + bytes(packet)
                packet_data = self.encrypt(packet_data)

                self.writer.write(packet_data)
                await self.writer.drain()
                if isinstance(packet, EncryptionResponse):
                    self.use_encryption = True
        except asyncio.CancelledError:
            self.writer.close()
            log.error("Writer : Write loop cancelled")
        except Exception:  # pylint: disable=broad-except
            log.exception("Writer : Error in write loop")
            await self.close()

    async def send_packet(self, packet: PACKET, *, immediate: bool = False) -> None:
        """
        Sends the given packet to the server.

        .. note::
            Unless ``immediate`` is ``True``, this does not wait for the packet to be sent.
            It instead adds the packet to a queue.
            Keep in mind that immediate will skip the queue and write the packet directly.

            If you want to ensure the packet is sent, you should consider using :meth:`wait_for`.

        :param packet: The packet to send.
        :type packet: Packet
        :param immediate: Whether to immediately write the packet or not.
        :type immediate: bool
        """
        if immediate:
            log.debug("Writer > Immediately sending %s", packet.__class__.__name__)
            packet_data = bytes(Varint(len(packet))) + bytes(packet)
            log.debug("Writer > Raw packet data: %s", packet_data)
            if self.cipher is not None:
                packet_data = self.encrypt(packet_data)
            self.writer.write(packet_data)
            await self.writer.drain()
        else:
            await self.outgoing_packets.put(packet)

    async def close(self, *, error: Exception = None):
        """
        Closes the connection.

        :param error: An error to raise after the connection is closed.
        :type error: Exception
        """
        log.info("Closing connection")
        if self._read_task:
            if not self._read_task.done():
                self._read_task.cancel()
        if self._write_task:
            if not self._read_task.done():
                self._write_task.cancel()
        if self._running:
            if error:
                self._running.set_exception(error)
            else:
                self._running.set_result(None)
        self.closed = True

    def change_state(self, state: State):
        self.state = state
        reactor = REACTORS.get(state)
        if reactor:
            reactor = reactor(self)
            reactor.setup()
        self.reactor = reactor
        log.info("Connection state changed to %s", state.name)

    async def wait_for_state(self, state: State, *, timeout: float = None) -> None:
        """
        Waits for the connection to change to the given state.

        :param state: The state to wait for.
        :type state: State
        :param timeout: The timeout in seconds.
        :type timeout: float

        :raises asyncio.TimeoutError: The timeout was reached.
        """
        if self.state == state:
            return
        timeout_at = time.time() + timeout if timeout is not None else None
        while self.state != state:
            await asyncio.sleep(0.01)
            if timeout_at is not None and time.time() > timeout_at:
                raise asyncio.TimeoutError(
                    "Timed out waiting for %s state" % state.name
                )

    # Login
    async def login(self):
        """
        Begins the login flow.

        :raises RuntimeError: The connection is not in the handshake state.
        :raises RuntimeError: The client does not have an access token set.
        """
        if self.state != State.HANDSHAKE:
            raise RuntimeError("Cannot begin login when not in handshake state")
        if self.client.access_token is None:
            raise RuntimeError("Cannot begin login without access token")
        log.info("Beginning standard login flow")
        await self.send_packet(
            Handshake(
                protocol_version=Varint(PROTOCOL_VERSION),
                server_address=String(self.host),
                server_port=UnsignedShort(self.port),
                next_state=NextState.LOGIN,
            ),
        )
        await self.wait_for_state(State.LOGIN)
        await self.send_packet(
            LoginStart(
                username=String(self.client.username),
                uuid=UUID.from_string(self.client.uuid),
            )
        )
