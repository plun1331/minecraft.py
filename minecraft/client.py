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
import traceback
from typing import Callable, Coroutine

from .auth import microsoft_auth
from .networking.connection import Connection
from .packets import Packet

log = logging.getLogger(__name__)


class Client:
    """
    The Minecraft client.

    This abstracts away the connection and provides a simple interface for
    sending and receiving packets.

    :ivar connection: The connection that this client uses. (:class:`Connection`)
    :ivar username: The username of the client. (:class:`str`)
    :ivar uuid: The UUID of the client. (:class:`str`)
    :ivar access_token: The access token of the client. 
        Used for authentication with the Mojang session server. (:class:`str`)

    """
    def __init__(self):
        self.connection: Connection = Connection(self)
        self.username: str | None = None
        self.uuid: str | None = None
        self.access_token: str | None = None

    # Base connection methods
    async def connect(self, host: str, port: int = 25565) -> None:
        """
        Connect to the server.

        Parameters
        ----------
        host: :class:`str`
            The host to connect to.
        port: :class:`int`
            The port to connect to.
        """
        await self.connection.connect(host, port)
        await self.connection.login()

    async def close(self) -> None:
        """
        Close the connection.
        """
        await self.connection.close()

    async def setup(self):
        """
        A utility method that is called before the connection is started.
        
        This takes no parameters and does nothing unless overridden.
        """
        pass

    async def start(self, host: str, port: int = 25565) -> None:
        """
        Setup the bot and connect to the server.

        This will also wait until the connection is closed before returning.

        Parameters
        ----------
        host: :class:`str`
            The host to connect to.
        port: :class:`int`
            The port to connect to.
        """
        await self.setup()
        await self.connect(host, port)
        await self.connection._running

    def run(self, host: str, port: int) -> None:
        """
        Run the bot.

        This will block until the connection is closed, 
        and will also handle keyboard interrupts and the event loop for you.

        Parameters
        ----------
        host: :class:`str`
            The host to connect to.
        port: :class:`int`
            The port to connect to.
        """
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(self.start(host, port))
        except KeyboardInterrupt:
            log.info("Got KeyboardInterrupt")
        finally:
            if not self.connection.closed:
                loop.run_until_complete(self.close())
            loop.close()

    # Authentication
    async def microsoft_auth(self, client_id: str) -> None:
        """
        Authenticate with Microsoft.

        Parameters
        ----------
        client_id: :class:`str`
            The client ID to use for authentication.
        """
        self.set_auth_info(*await microsoft_auth(client_id))

    def set_auth_info(self, username: str, uuid: str, access_token: str) -> None:
        """
        Set the authentication information.
        
        Parameters
        ----------
        username: :class:`str`
            The username of the client.
        uuid: :class:`str`
            The UUID of the client.
        access_token: :class:`str`
            The access token of the client. Used to authenticate with Mojang.
        """
        self.username = username
        self.uuid = uuid
        self.access_token = access_token

    # Handlers

    async def handler_error(self, handler, error: Exception) -> None:
        """
        Called whenever a packet handler raises an exception.

        The default behavior is to print the traceback.

        Parameters
        ----------
        handler: :class:`str`
            The name of the handler.
        error: :class:`Exception`
            The exception that was raised.
        """
        print(f"Error in handler {handler}:")
        traceback.print_exception(type(error), error, error.__traceback__)

    async def wait_for_packet(
        self, packet_type: type[Packet], *, timeout: float = None
    ) -> Packet:
        """
        Wait for a packet to be received.

        :param packet_type: The type of packet to wait for.
        :type packet_type: type[Packet]
        :param timeout: The amount of time to wait before timing out.
        :type timeout: float
        
        :return: The packet that was received.
        :rtype: Packet

        :raises asyncio.TimeoutError: The packet was not received before the timeout.
        """
        return await self.connection.dispatcher.wait_for(packet_type, timeout=timeout)

    def add_handler(
        self, packet_type: type[Packet], handler: Callable[[Packet], Coroutine[None, None, None]]
    ) -> None:
        """
        Add a packet handler.
        
        :param packet_type: The type of packet to handle.
        :type packet_type: type[Packet]
        :param handler: The handler to call when the packet is received.
            Must be an async function.
        :type handler: Callable[[Packet], Coroutine[None, None, None]]
        """
        self.connection.dispatcher.register(packet_type, handler)

    def remove_handler(
        self, packet_type: type[Packet], handler: Callable[[Packet], Coroutine[None, None, None]]
    ) -> None:
        """
        Removes a handler for a packet.

        :param packet_type: The packet that the handler is reacting to.
        :type packet_type: type[Packet]
        :param handler: The handler that should be removed.
        :type handler: Callable[[Packet], Coroutine[None, None, None]]

        :raises ValueError: The handler is not registered for the packet.
        """
        return self.connection.dispatcher.remove_handler(packet_type, handler)

    def handle(self, packet_type: type[Packet]) -> Callable[[Callable[[Packet], Coroutine[None, None, None]]], Callable[[Packet], Coroutine[None, None, None]]]:
        """
        A decorator that adds a packet handler.

        :param packet_type: The type of packet to handle.
        :type packet_type: type[Packet]
        """
        def decorator(handler: Callable[[Packet], Coroutine[None, None, None]]) -> Callable[[Packet], Coroutine[None, None, None]]:
            self.add_handler(packet_type, handler)
            return handler
        return decorator
    
    # Packets
    async def send_packet(self, packet: Packet) -> None:
        """
        Send a packet to the server.

        .. note::
            This does not wait for the packet to send.
            Instead, it adds it to a queue.

        :param packet: The packet to send.
        :type packet: Packet
        """
        await self.connection.send_packet(packet)
