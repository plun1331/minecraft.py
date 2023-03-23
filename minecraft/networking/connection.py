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
import zlib
from typing import TYPE_CHECKING

from cryptography.hazmat.primitives.ciphers import Cipher, CipherContext

from minecraft.packets.login_serverbound import EncryptionResponse
from .dispatcher import Dispatcher
from .reactors import REACTORS
from .reactors.base import REACTOR
from ..datatypes import *
from ..enums import NextState, State
from ..exceptions import PacketTooLargeError, UnknownPacketError
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
    def __init__(self, client):
        self.client: Client = client
        self.state: State = State.HANDSHAKE
        self.loop: asyncio.AbstractEventLoop | None = None
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.read_task: asyncio.Task | None = None
        self.write_task: asyncio.Task | None = None
        self.outgoing_packets: asyncio.Queue[PACKET] = asyncio.Queue()
        self.dispatcher: Dispatcher = Dispatcher(self)
        self.host: str | None = None
        self.port: int | None = None
        self.shared_secret: bytes | None = None
        self.cipher: Cipher | None = None
        self.use_encryption: bool = False
        self.reactor: REACTOR | None = None
        self._running: asyncio.Future | None = asyncio.Future()
        self.closed: bool = False
        self.encryptor: CipherContext | None = None
        self.decryptor: CipherContext | None = None
        self.compression_threshold: int = 0
        self.use_compression: bool = False
        self.compression_object = zlib.compressobj()
        self.decompression_object = zlib.decompressobj()

    def encrypt(self, data: bytes) -> bytes:
        if not self.use_encryption:
            return data
        if self.encryptor is None:
            raise RuntimeError("Cannot encrypt without an encryptor")
        return self.encryptor.update(data)

    def decrypt(self, data: bytes) -> bytes:
        if not self.use_encryption:
            return data
        if self.decryptor is None:
            raise RuntimeError("Cannot decrypt without a decryptor")
        return self.decryptor.update(data)

    def compress(self, data: bytes) -> tuple[bytes, bool]:
        if not self.use_compression:
            return data, False
        if len(data) < self.compression_threshold:
            return data, False
        return self.compression_object.compress(data), True

    def decompress(self, data: bytes) -> bytes:
        if not self.use_compression:
            return data
        return self.decompression_object.decompress(data)

    async def connect(self, host: str, port: int):
        log.info(
            f"Connecting to {host}:{port} with protocol version {PROTOCOL_VERSION} ({RELEASE_NAME})"
        )
        self.host = host
        self.port = port
        self.loop = asyncio.get_running_loop()
        self._running = asyncio.Future()
        self.reader, self.writer = await asyncio.open_connection(host, port)
        self.read_task = self.loop.create_task(self._read_loop())
        self.write_task = self.loop.create_task(self._write_loop())
        log.info("Started read/write tasks")

    async def parse_varint(self) -> int:
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
        return result

    async def _read_loop(self):
        try:
            while True:
                packet_length = await self.parse_varint()
                data_length = 0
                if self.use_compression:
                    data_length = await self.parse_varint()
                log.debug(
                    f"Reader < Recieving packet of compressed length {packet_length} (uncompressed {data_length})"
                )
                if packet_length > 2097151 or data_length > 2097151:
                    log.error(
                        f"Reader x< Packet length {packet_length} is too large, terminating connection"
                    )
                    await self.close(
                        error=PacketTooLargeError(
                            f"Packet length of {packet_length} is too large"
                        )
                    )
                    return

                packet_data = self.decrypt(await self.reader.readexactly(packet_length))
                if data_length > 0:
                    packet_data = self.decompress(packet_data)
                    if len(packet_data) != data_length:
                        log.error(
                            f"Reader x< Packet length {packet_length} does not match "
                            f"expected uncompressed length {data_length}, terminating connection"
                        )
                        await self.close(
                            error=PacketTooLargeError(
                                f"Packet length of {packet_length} did not match expected length of {data_length}"
                            )
                        )
                        return
                try:
                    packet = get_packet(packet_data, state=self.state)
                except KeyError:
                    log.error(
                        f"Reader < Recieved unknown packet with id "
                        f"{Varint.from_bytes(BytesIO(packet_data)).value}"
                    )
                    await self.close(
                        error=UnknownPacketError(
                            "Unknown packet recieved from server",
                            packet_id=Varint.from_bytes(BytesIO(packet_data)).value,
                            data=packet_data,
                        )
                    )
                    return

                log.debug(f"Reader < Recieved {packet.__class__.__name__}")
                self.dispatcher.dispatch(packet)
        except asyncio.CancelledError:
            log.error("Reader : Read loop cancelled")
        except Exception:
            log.exception("Reader : Error in read loop")
            await self.close()

    async def _write_loop(self):
        try:
            while True:
                packet: PACKET = await self.outgoing_packets.get()
                if packet.state != self.state:
                    log.error(
                        f"Writer x> Illegal packet {packet.__class__.__name__} "
                        f" during {self.state.name} (expected state {packet.state.name})"
                    )
                    continue
                if isinstance(packet, Handshake):
                    self.change_state(State.from_value(packet.next_state.value))

                log.debug(
                    f"Writer > Sending {packet.__class__.__name__} ({packet.packet_id})"
                )
                packet_length = len(packet)
                if packet_length > 2097151:
                    log.error(
                        f"Writer x> Packet length {packet_length} is too large, terminating connection"
                    )
                    await self.close(
                        error=PacketTooLargeError(
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
        except Exception:
            log.exception("Writer : Error in write loop")
            await self.close()

    async def send_packet(self, packet: PACKET, *, immediate: bool = False):
        if immediate:
            log.debug(f"Writer > Immediately sending {packet.__class__.__name__}")
            packet_data = bytes(Varint(len(packet))) + bytes(packet)
            log.debug(f"Writer > Raw packet data: {packet_data}")
            if self.cipher is not None:
                packet_data = self.encrypt(packet_data)
            self.writer.write(packet_data)
            await self.writer.drain()
        else:
            await self.outgoing_packets.put(packet)

    async def close(self, *, error: Exception = None):
        log.info("Closing connection")
        if self.read_task:
            if not self.read_task.done():
                self.read_task.cancel()
        if self.write_task:
            if not self.read_task.done():
                self.write_task.cancel()
        if error:
            self._running.set_exception(error)
        else:
            self._running.set_result(None)
        self.closed = True

    def change_state(self, state: State):
        self.state = state
        if self.reactor:
            self.reactor.destroy()
        reactor = REACTORS.get(state)
        if reactor:
            reactor = reactor(self)
            reactor.setup()
        self.reactor = reactor
        log.info(f"Connection state changed to {state.name}")

    async def wait_for(self, packet: type[Packet], *, timeout: float = None) -> PACKET:
        return await self.dispatcher.wait_for(packet, timeout=timeout)

    async def wait_for_state(self, state: State, *, timeout: float = None):
        if self.state == state:
            return
        timeout_at = time.time() + timeout if timeout is not None else None
        while self.state != state:
            await asyncio.sleep(0.01)
            if timeout_at is not None and time.time() > timeout_at:
                raise asyncio.TimeoutError(f"Timed out waiting for state {state.name}")

    # Login
    async def login(self):
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
