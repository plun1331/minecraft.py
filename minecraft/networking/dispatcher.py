import asyncio
import logging
from typing import Callable, Coroutine

from ..packets import Packet, PACKET

log = logging.getLogger(__name__)


class Dispatcher:
    def __init__(self, connection):
        self.connection = connection
        self.handlers: dict[type[Packet], list] = {}
        self.temporary_handlers: dict[type[Packet], asyncio.Future] = {}

    def register(
        self, packet: type[Packet], handler: Callable[[Packet], Coroutine]
    ) -> None:
        """
        Register a handler for a packet.

        Parameters
        ----------
        packet: :class:`Packet`
            The packet that the handler should react to.
        handler: Callable[[Packet], Coroutine]
            The handler that should be called when the packet is received.
        """
        if packet not in self.handlers:
            self.handlers[packet] = []
        self.handlers[packet].append(handler)

    def remove_handler(
        self, packet: type[Packet], handler: Callable[[Packet], Coroutine]
    ) -> None:
        """
        Remove a handler for a packet.

        Parameters
        ----------
        packet: :class:`Packet`
            The packet that the handler is reacting to.
        handler: Callable[[Packet], Coroutine]
            The handler that should be removed.

        Raises
        ------
        :exc:`ValueError`
            The handler is not registered for the packet.
        """
        if packet in self.handlers:
            self.handlers[packet].remove(handler)

    async def _handler_wrapper(
        self, packet: PACKET, handler: Callable[[Packet], Coroutine]
    ) -> None:
        try:
            await handler(packet)
        except Exception as e:  # pylint: disable=broad-except
            await self.connection.client.handler_error(handler, e)

    def dispatch(self, packet) -> None:
        """
        Dispatch a packet to the appropriate handlers.

        Parameters
        ----------
        packet: :class:`Packet`
            The packet to dispatch.
        """
        log.debug("Dispatching packet %s", packet)
        if packet.__class__ in self.handlers:
            for handler in self.handlers[packet.__class__]:
                self.connection.loop.create_task(
                    self._handler_wrapper(packet, handler),
                    name=f"handle-{packet.__class__.__name__}-{handler.__name__}",
                )
        if packet.__class__ in self.temporary_handlers:
            self.temporary_handlers[packet.__class__].set_result(packet)
            self.temporary_handlers.pop(packet.__class__, None)

    async def wait_for(self, packet_id, *, timeout=None) -> PACKET:
        """
        Wait for a packet to be received.

        Parameters
        ----------
        packet_id: :class:`int`
            The packet ID to wait for.
        timeout: :class:`float`
            The amount of time to wait before timing out.

        Returns
        -------
        :class:`Packet`
            The packet that was received.

        Raises
        ------
        :exc:`asyncio.TimeoutError`
            The packet was not received before the timeout.
        """
        if packet_id not in self.temporary_handlers:
            self.temporary_handlers[packet_id] = asyncio.Future()
        return await asyncio.wait_for(
            self.temporary_handlers[packet_id], timeout=timeout
        )
