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
import logging
import time
from typing import TYPE_CHECKING

from cryptography.hazmat.primitives.ciphers import Cipher

from minecraft.packets.login_serverbound import EncryptionResponse
from .dispatcher import Dispatcher
from .reactors import REACTORS
from .reactors.base import REACTOR
from ..datatypes import *
from ..enums import NextState, State
from ..packets import (
    get_packet,
    Handshake,
    LoginStart,
    Packet,
    PACKET,
)

if TYPE_CHECKING:
    from ..client import Client

log = logging.getLogger(__name__)

PROTOCOL_VERSION: int = 761
RELEASE_NAME: str = "1.19.3"


class Connection:
    """
    Handles sending and recieving packets from the server.

    Attributes  
    ----------
    client: :class:`Client`
        The client that this connection is attached to.
    host: :class:`str`
        The host that the connection is connected to.
    port: :class:`int`
        The port that the connection is on.
    state: :class:`State`
        The current state of the connection.
    closed: :class:`bool`
        Whether or not the connection has been closed.
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop that the connection is running on.
    reader: :class:`asyncio.StreamReader`
        The reader that the connection is using to read packets.
    writer: :class:`asyncio.StreamWriter`
        The writer that the connection is using to write packets.
    outgoing_packets: :class:`asyncio.Queue`
        The queue of packets that are waiting to be sent.
    dispatcher: :class:`Dispatcher`
        The dispatcher that is handling incoming packets.
    using_compression: :class:`bool`
        Whether or not the connection is using compression.
    use_encryption: :class:`bool`
        Whether or not the connection is using encryption.
    shared_secret: :class:`bytes`
        The shared secret that is being used for encryption.
    cipher: :class:`cryptography.hazmat.primitives.ciphers.Cipher`
        The cipher that is being used for encryption.
    reactor: :class:`Reactor`
        The reactor that currently has registered packet listeners.
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
        self.outgoing_packets: asyncio.Queue[type[Packet]] = asyncio.Queue()
        self.dispatcher: Dispatcher = Dispatcher(self)
        self.reactor: REACTOR | None = None

        self.using_compression: bool = False

        self.use_encryption: bool = False
        self.shared_secret: bytes | None = None
        self.cipher: Cipher | None = None

        self._running: asyncio.Future | None = None
        self._read_task: asyncio.Task | None = None
        self._write_task: asyncio.Task | None = None

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypts the given data using the connection's cipher.
        
        Parameters
        ----------
        data: :class:`bytes`
            The data to encrypt.
            
        Returns
        -------
        :class:`bytes`
            The encrypted data.
        """
        if not self.use_encryption:
            return data
        if self.shared_secret is None:
            raise RuntimeError("Cannot encrypt data before shared secret is set")
        encryptor = self.cipher.encryptor()
        return encryptor.update(data)

    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypts the given data using the connection's cipher.

        Parameters
        ----------
        data: :class:`bytes`
            The data to decrypt.

        Returns
        -------
        :class:`bytes`
            The decrypted data.
        """
        if not self.use_encryption:
            return data
        if self.shared_secret is None:
            raise RuntimeError("Cannot decrypt data before shared secret is set")
        decryptor = self.cipher.decryptor()
        return decryptor.update(data)

    async def connect(self, host: str, port: int) -> None:
        """
        Connects to the given host and port.
        
        Parameters
        ----------
        host: :class:`str`
            The host to connect to.
        port: :class:`int`
            The port to connect to.
        """
        log.info(
            f"Connecting to {host}:{port} with protocol version {PROTOCOL_VERSION} ({RELEASE_NAME})"
        )
        self.host = host
        self.port = port
        self.loop = asyncio.get_running_loop()
        self._running = asyncio.Future()
        self.reader, self.writer = await asyncio.open_connection(host, port)
        self._read_task = self.loop.create_task(self._read_loop())
        self._write_task = self.loop.create_task(self._write_loop())
        log.info("Started read/write tasks")

    async def _read_loop(self) -> None:
        try:
            while True:
                num_read = 0
                result = 0
                # Manually parse out a varint
                while True:
                    read = await self.reader.read(1)
                    if read == b"":
                        await asyncio.sleep(0.01)
                        continue
                    read = self.decrypt(read)
                    value = read[0] & 0b01111111
                    result |= value << (7 * num_read)
                    num_read += 1
                    if (read[0] & 0b10000000) == 0:
                        break
                packet_length = result
                log.debug("Reader < Recieving packet of length %s", packet_length)
                packet_data = self.decrypt(await self.reader.read(packet_length))
                try:
                    packet = get_packet(packet_data, state=self.state)
                except KeyError:
                    log.error(
                        "Reader < Recieved unknown packet with id "
                        "%s: %s",
                        Varint.from_bytes(BytesIO(packet_data)).value,
                        packet_data,
                    )
                    continue

                log.debug("Reader < Recieved %s", packet.__class__.__name__)
                self.dispatcher.dispatch(packet)
        except asyncio.CancelledError:
            log.error("Reader : Read loop cancelled")
            self.reader.feed_eof()
        except Exception:  # pylint: disable=broad-except
            log.exception("Reader : Error in read loop")

    async def _write_loop(self) -> None:
        try:
            while True:
                packet: PACKET = await self.outgoing_packets.get()
                if packet.state != self.state:
                    log.error(
                        "Writer x> Illegal packet %s "
                        " during %s (expected state %s)",
                        packet.__class__.__name__,
                        self.state.name,
                        packet.state.name,
                    )
                    continue
                if isinstance(packet, Handshake):
                    self.change_state(State.from_value(packet.next_state.value))

                log.debug(
                    "Writer > Sending %s (%s)", packet.__class__.__name__, packet.packet_id
                )
                packet_data = bytes(Varint(len(packet))) + bytes(packet)
                packet_data = self.encrypt(packet_data)

                if isinstance(packet, EncryptionResponse):
                    self.use_encryption = True

                self.writer.write(packet_data)
                await self.writer.drain()
        except asyncio.CancelledError:
            self.writer.close()
            log.error("Writer : Write loop cancelled")
        except Exception:  # pylint: disable=broad-except
            log.exception("Writer : Error in write loop")

    async def send_packet(self, packet: PACKET, *, immediate: bool = False) -> None:
        """
        Sends the given packet to the server.

        .. note::
            Unless ``immediate`` is ``True`, this does not wait for the packet to be sent.
            It instead adds the packet to a queue.

            If you want to ensure the packet is sent, you should consider using :meth:`wait_for`.
        
        Parameters
        ----------
        packet: :class:`Packet`
            The packet to send.
        immediate: :class:`bool`
            Whether to immediately write the packet or not.
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

        Parameters
        ----------
        error: :class:`Exception`
            An error to raise after the connection is closed.
        """
        log.info("Closing connection")
        if self._read_task:
            self._read_task.cancel()
            await self._read_task
        if self._write_task:
            self._write_task.cancel()
            await self._write_task
        if error:
            self._running.set_exception(error)
        else:
            self._running.set_result(None)
        self.closed = True

    def change_state(self, state: State):
        """
        Changes the connection state.

        This method should never be used except when connecting to the server.
        
        Parameters
        ----------
        state: :class:`State`
            The new state to change to.
        """
        self.state = state
        if self.reactor:
            self.reactor.destroy()
        self.reactor = REACTORS.get(state)(self)
        if self.reactor:
            self.reactor.setup()
        log.info("Connection state changed to %s", state.name)

    async def wait_for_state(self, state: State, *, timeout: float = None) -> None:
        """
        Waits for the connection to change to the given state.

        Parameters
        ----------
        state: :class:`State`
            The state to wait for.
        timeout: :class:`float`
            The timeout in seconds.

        Raises
        ------
        :exc:`asyncio.TimeoutError`
            The timeout was reached.
        """
        if self.state == state:
            return
        timeout_at = time.time() + timeout if timeout is not None else None
        while self.state != state:
            await asyncio.sleep(0.01)
            if timeout_at is not None and time.time() > timeout_at:
                raise asyncio.TimeoutError("Timed out waiting for %s state" % state.name)

    # Login
    async def login(self):
        """
        Begins the login flow.

        Raises
        ------
        :exc:`RuntimeError`
            The connection is not in the handshake state.
        :exc:`RuntimeError`
            The client does not have an access token set.
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
