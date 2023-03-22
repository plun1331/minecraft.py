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

import logging
import asyncio
import traceback
from typing import Callable, Coroutine

from .auth import microsoft_auth
from .networking.connection import Connection
from .packets import Packet

log = logging.getLogger(__name__)


class Client:
    def __init__(self):
        self.connection: Connection = Connection(self)
        self.username: str | None = None
        self.uuid: str | None = None
        self.access_token: str | None = None
        self.listeners: dict[
            type[Packet], list[Callable[[Packet], Coroutine[None, None, None]]]
        ] = {}

    async def connect(self, host: str, port: int = 25565) -> None:
        await self.connection.connect(host, port)
        await self.connection.login()

    async def microsoft_auth(self, client_id: str) -> None:
        self.username, self.uuid, self.access_token = await microsoft_auth(client_id)

    async def close(self) -> None:
        await self.connection.close()

    async def _dispatch_listener(self, packet: Packet, listener: Callable) -> None:
        log.debug(f"Dispatching {packet} to {listener}")
        try:
            await listener(packet)
        except Exception as e:
            await self.handle_listener_error(listener, e)

    async def handle_listener_error(self, listener: Callable, error: Exception) -> None:
        print(f"Error in listener {listener}:")
        traceback.print_exc()

    async def handle_packet(self, packet: Packet) -> None:
        log.debug(f"Dispatching {packet.__class__.__name__} to all listeners")
        for listener in self.listeners.get(type(packet), []):
            self.connection.loop.create_task(self._dispatch_listener(packet, listener))

    async def wait_for_packet(
        self, packet_type: type[Packet], *, timeout: float = None
    ) -> Packet:
        return await self.connection.wait_for(packet_type, timeout=timeout)
    
    async def setup(self):
        pass

    async def start(self, host: str, port: int = 25565) -> None:
        await self.setup()
        await self.connect(host, port)
    
    def run(self, host: str, port: int) -> None:
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(self.start(host, port))
            loop.run_forever()
        except KeyboardInterrupt:
            log.info("Got KeyboardInterrupt")
        finally:
            loop.run_until_complete(self.close())
            loop.close()    
