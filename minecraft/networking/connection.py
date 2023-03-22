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

from typing import TYPE_CHECKING
from cryptography.hazmat.primitives.ciphers import Cipher
from ..enums import State, NextState
from ..datatypes import *
from .dispatcher import Dispatcher
from ..packets import (
    get_packet, 
    Packet, 
    Handshake, 
    DisconnectLogin, 
    LoginStart,
    EncryptionRequest,
    LoginSuccess,
    LoginPluginResponse,
    LoginPluginRequest,
)
from .reactors.base import REACTOR
from .reactors import REACTORS

if TYPE_CHECKING:
    from ..client import Client


log = logging.getLogger(__name__)

PROTOCOL_VERSION: int = 762
RELEASE_NAME: str = "1.19.4"


class Connection:
    def __init__(self, client):
        self.client: Client = client
        self.state: State = State.HANDSHAKE
        self.loop: asyncio.AbstractEventLoop | None = None
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.read_task: asyncio.Task | None = None
        self.write_task: asyncio.Task | None = None
        self.outgoing_packets: asyncio.Queue[type[Packet]] = asyncio.Queue()
        self.dispatcher: Dispatcher = Dispatcher(self)
        self.using_compression: bool = False
        self.host: str | None = None
        self.port: int | None = None
        self.shared_secret: bytes | None = None
        self.cipher: Cipher | None = None
        self.reactor: REACTOR | None = None

    def encrypt(self, data: bytes) -> bytes:
        if self.shared_secret is None:
            raise RuntimeError("Cannot encrypt data before shared secret is set")
        encryptor = self.cipher.encryptor()
        return encryptor.update(data)
    
    def decrypt(self, data: bytes) -> bytes:
        if self.shared_secret is None:
            raise RuntimeError("Cannot decrypt data before shared secret is set")
        decryptor = self.cipher.decryptor()
        return decryptor.update(data)

    async def connect(self, host: str, port: int):
        log.info(f"Connecting to {host}:{port} with protocol version {PROTOCOL_VERSION} ({RELEASE_NAME})")
        self.host = host
        self.port = port
        self.loop = asyncio.get_running_loop()
        self.reader, self.writer = await asyncio.open_connection(host, port)
        self.read_task = self.loop.create_task(self._read_loop())
        self.write_task = self.loop.create_task(self._write_loop())
        log.info("Started read/write tasks")

    async def _read_loop(self):
        try:
            while True:
                num_read = 0
                result = 0
                while True:
                    read = await self.reader.read(1)
                    if read == b"":
                        continue
                    if self.cipher is not None:
                        read = self.decrypt(read)
                    log.debug(f"Connection (raw) < {read}")
                    value = read[0] & 0b01111111
                    result |= value << (7 * num_read)
                    num_read += 1
                    if (read[0] & 0b10000000) == 0:
                        break
                packet_length = result
                packet_data = await self.reader.read(packet_length)
                if self.cipher is not None:
                    packet_data = self.decrypt(packet_data)
                log.debug(f"Connection (raw) < {packet_data}")
                packet = get_packet(BytesIO(packet_data))
                log.debug(f"Connection < {packet}")
                self.dispatcher.dispatch(packet)
        except asyncio.CancelledError:
            log.error("Read loop cancelled")
            self.reader.feed_eof()
        except KeyboardInterrupt:
            self.reader.feed_eof()
            await self.client.close()
        except Exception:
            log.exception("Error in read loop", exc_info=True)

    async def _write_loop(self):
        try:
            while True:
                packet = await self.outgoing_packets.get()
                log.debug(f"Connection > {packet}")
                packet_data = bytes(Varint(len(packet))) + bytes(packet)
                log.debug(f"Connection (raw) > {packet_data}")
                if self.cipher is not None:
                    packet_data = self.encrypt(packet_data)
                self.writer.write(packet_data)
                await self.writer.drain()
        except asyncio.CancelledError:
            self.writer.close()
        except Exception:
            log.exception("Error in read loop", exc_info=True)

    async def send_packet(self, packet: type[Packet], *, immediate: bool = False):
        if immediate:
            log.debug(f"Connection I> {packet}")
            packet_data = bytes(Varint(len(packet))) + bytes(packet)
            log.debug(f"Connection (raw) I> {packet_data}")
            if self.cipher is not None:
                packet_data = self.encrypt(packet_data)
            self.writer.write(packet_data)
            await self.writer.drain()
        else:
            await self.outgoing_packets.put(packet)

    async def close(self):
        log.info("Closing connection")
        if self.read_task:
            self.read_task.cancel()
            await self.read_task
        if self.write_task:
            self.write_task.cancel()
            await self.write_task

    def change_state(self, state: State):
        self.state = state
        self.reactor = REACTORS.get(state)
        log.info(f"State changed to {state.name}")

    async def wait_for(self, packet: type[Packet], *, timeout: float = None) -> type[Packet]:
        await self.dispatcher.wait_for(packet, timeout=timeout)

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
                next_state=NextState.LOGIN
            ),
        )
        self.change_state(State.LOGIN)
        await self.send_packet(
            LoginStart(
                username=String(self.client.username), 
                uuid=UUID.from_string(self.client.uuid)
            )
        )
