

import asyncio
import logging
from typing import Callable, Coroutine
from ..packets.base import Packet


log = logging.getLogger(__name__)

class Dispatcher:
    def __init__(self, connection):
        self.connection = connection
        self.handlers: dict[type[Packet], list] = {}
        self.temporary_handlers: dict[type[Packet], asyncio.Future] = {}

    def register(self, packet: type[Packet], handler: Callable[[Packet], Coroutine]):
        if packet not in self.handlers:
            self.handlers[packet] = []
        self.handlers[packet].append(handler)

    def remove_handler(self, packet: type[Packet], handler: Callable[[Packet], Coroutine]):
        if packet in self.handlers:
            self.handlers[packet].remove(handler)

    async def handler_wrapper(self, packet, handler):
        try:
            await handler(packet)
        except Exception as e:
            await self.connection.client.handler_error(e)

    def dispatch(self, packet):
        log.debug(f"Dispatching {packet}")
        if packet.__class__ in self.handlers:
            for handler in self.handlers[packet.__class__]:
                self.connection.loop.create_task(
                    self.handler_wrapper(packet, handler), 
                    name=f"handle-{packet.__class__.__name__}-{handler.__name__}"
                )
        if packet.__class__ in self.temporary_handlers:
            self.temporary_handlers[packet.__class__].set_result(packet)
            self.temporary_handlers.pop(packet.__class__, None)

    async def wait_for(self, packet_id, *, timeout=None):
        if packet_id not in self.temporary_handlers:
            self.temporary_handlers[packet_id] = asyncio.Future()
        return await asyncio.wait_for(self.temporary_handlers[packet_id], timeout=timeout)
        