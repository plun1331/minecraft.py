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
from typing import Callable, Coroutine, TYPE_CHECKING

from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes

from .encryption import process_encryption_request
from ..datatypes import *
from ..enums import NextState, State
from ..packets import (
    DisconnectLogin,
    EncryptionRequest,
    EncryptionResponse,
    get_packet,
    Handshake,
    LoginPluginRequest,
    LoginPluginResponse,
    LoginStart,
    LoginSuccess,
    Packet,
    PACKET,
)

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
        self.outgoing_packets: asyncio.Queue[PACKET] = asyncio.Queue()
        self.default_recieve_handlers: dict[
            type[PACKET], Callable[[PACKET], Coroutine]
        ] = {
            LoginPluginRequest: self._handle_login_plugin_request,
            DisconnectLogin: self._handle_disconnect_login,
        }
        self.using_compression: bool = False
        self.host: str | None = None
        self.port: int | None = None
        self.temporary_listeners: dict[type[PACKET], asyncio.Future] = {}
        self.shared_secret: bytes | None = None
        self.cipher: Cipher | None = None
        self.use_encryption: bool = False

    def encrypt(self, data: bytes) -> bytes:
        if not self.use_encryption:
            return data
        if self.shared_secret is None:
            raise RuntimeError("Cannot encrypt data before shared secret is set")
        encryptor = self.cipher.encryptor()
        return encryptor.update(data)

    def decrypt(self, data: bytes) -> bytes:
        if not self.use_encryption:
            return data
        if self.shared_secret is None:
            raise RuntimeError("Cannot decrypt data before shared secret is set")
        decryptor = self.cipher.decryptor()
        return decryptor.update(data)

    async def connect(self, host: str, port: int):
        log.info(
            f"Connecting to {host}:{port} with protocol version {PROTOCOL_VERSION} ({RELEASE_NAME})"
        )
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
                        await asyncio.sleep(0.01)
                        continue
                    read = self.decrypt(read)
                    value = read[0] & 0b01111111
                    result |= value << (7 * num_read)
                    num_read += 1
                    if (read[0] & 0b10000000) == 0:
                        break
                packet_length = result
                log.debug(f"Connection < Recieving packet of length {packet_length}")
                untouched_packet_data = await self.reader.read(packet_length)

                packet_data = self.decrypt(untouched_packet_data)
                try:
                    packet = get_packet(packet_data, state=self.state)
                except KeyError:
                    try:
                        packet = get_packet(untouched_packet_data, state=self.state)
                    except KeyError:
                        log.error(
                            f"Connection < Recieved unknown packet with id "
                            f"{Varint.from_bytes(BytesIO(packet_data)).value}: {packet_data}"
                        )
                        continue
                log.debug(
                    f"Connection < Recieved {packet.__class__.__name__} ({packet.packet_id})"
                )
                if type(packet) in self.default_recieve_handlers:
                    log.debug(
                        f"Connection : Dispatching default handler for {packet.__class__.__name__}"
                    )
                    await self.default_recieve_handlers[packet.__class__](packet)
                elif type(packet) in self.temporary_listeners:
                    log.debug(
                        f"Connection : Dispatching temporary listener for {packet}"
                    )
                    self.temporary_listeners[packet.__class__].set_result(packet)
                await self.client.handle_packet(packet)
        except asyncio.CancelledError:
            log.error("Connection : Read loop cancelled")
            self.reader.feed_eof()
        except KeyboardInterrupt:
            self.reader.feed_eof()
            await self.client.close()
        except Exception:
            log.exception("Connection : Error in read loop")

    async def _write_loop(self):
        try:
            while True:
                packet: PACKET = await self.outgoing_packets.get()
                if packet.state != self.state:
                    log.error(
                        f"Connection : Illegal packet {packet.__class__.__name__} "
                        f" during {self.state.name} (expected state {packet.state.name})"
                    )
                    continue
                if isinstance(packet, Handshake):
                    self.change_state(State.from_value(packet.next_state.value))
                log.debug(
                    f"Connection > Sending {packet.__class__.__name__} ({packet.packet_id})"
                )
                packet_data = bytes(Varint(len(packet))) + bytes(packet)
                log.debug(
                    f"Connection > Raw packet data: {packet_data} ({len(packet_data)} - {len(packet)})"
                )
                packet_data = self.encrypt(packet_data)
                if isinstance(packet, EncryptionResponse):
                    self.use_encryption = True
                self.writer.write(packet_data)
                await self.writer.drain()
        except asyncio.CancelledError:
            self.writer.close()
        except Exception:
            log.exception("Connection : Error in write loop")

    async def send_packet(self, packet: PACKET, *, immediate: bool = False):
        if immediate:
            log.debug(f"Connection > Immediately sending {packet.__class__.__name__}")
            packet_data = bytes(Varint(len(packet))) + bytes(packet)
            log.debug(f"Connection > Raw packet data: {packet_data}")
            if self.cipher is not None:
                packet_data = self.encrypt(packet_data)
            self.writer.write(packet_data)
            await self.writer.drain()
        else:
            await self.outgoing_packets.put(packet)

    async def close(self):
        log.info("Closing connection")
        self.read_task.cancel()
        self.write_task.cancel()
        await self.read_task
        await self.write_task
        self.loop.close()

    def change_state(self, state: State):
        self.state = state
        log.info(f"Connection : State changed to {state.name}")

    async def wait_for(self, packet: type[Packet], *, timeout: float = None) -> PACKET:
        if packet in self.temporary_listeners:
            return await asyncio.wait_for(
                self.temporary_listeners[packet], timeout=timeout
            )
        future = self.loop.create_future()
        self.temporary_listeners[packet] = future
        log.debug(f"Connection : Waiting for {packet} (timeout: {timeout})")
        try:
            result = await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError as e:
            raise asyncio.TimeoutError(f"Timed out waiting for {packet}") from e
        finally:
            del self.temporary_listeners[packet]
        return result

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
        log.info("Connection : Beginning standard login flow")
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
        try:
            encryption_request = await self.wait_for(EncryptionRequest, timeout=30)
        except asyncio.TimeoutError as e:
            log.warning(
                f"Connection : Server did not send encryption request, terminating connection"
            )
            raise asyncio.TimeoutError("Server did not send encryption request") from e
        encryption_data = await process_encryption_request(encryption_request, self)
        await self.send_packet(
            EncryptionResponse(
                shared_secret=ByteArray(encryption_data["encrypted_shared_secret"]),
                verify_token=ByteArray(encryption_data["encrypted_verify_token"]),
            )
        )
        self.shared_secret = encryption_data["shared_secret"]
        self.cipher = Cipher(
            algorithms.AES(self.shared_secret), modes.CFB8(self.shared_secret)
        )
        login_success = await self.wait_for(LoginSuccess)
        self.client.uuid = login_success.uuid
        self.client.username = login_success.username
        self.client.properties = login_success.properties
        log.info("Login successful")

    async def _handle_disconnect_login(self, packet: DisconnectLogin):
        log.info(f"Connection : Disconnected from server: {packet.reason.value}")
        await self.close()

    async def _handle_login_plugin_request(self, packet: LoginPluginRequest):
        await self.send_packet(
            LoginPluginResponse(message_id=packet.message_id, successful=Boolean(False))
        )

    async def _handle_login_success(self, packet: LoginSuccess):
        log.info(f"Connection : Login successful as {packet.username}")
        self.change_state(State.PLAY)
