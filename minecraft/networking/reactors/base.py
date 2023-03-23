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

from typing import Callable, TYPE_CHECKING, TypeVar

from ...packets import Packet, PACKET

if TYPE_CHECKING:
    from ..connection import Connection
    from ...client import Client


def react_to(
    packet: type[Packet],
) -> Callable[[Callable[[PACKET], None]], Callable[[PACKET], None]]:
    """
    Decorator for specifying what packets a method in a :class:`Reactor` should react to.

    Parameters
    ----------
    packet: :class:`Packet`
        The packet that the method should react to.
    """
    def decorator(func: Callable[[PACKET], None]) -> Callable[[PACKET], None]:
        func.__reacts_to__ = packet
        return func

    return decorator


class Reactor:
    """
    Base class for all reactors.

    Reactors are used to handle packets internally,
    though they can be overwritten to change their behavior.

    Attributes
    ----------
    connection: :class:`Connection`
        The connection that this reactor is attached to.
    """
    def __init__(self, connection) -> None:
        self.connection: Connection = connection

    def setup(self):
        """
        Setup the reactor.

        This method is called when the reactor is attached to a connection.
        """
        for name in dir(self):
            attr = getattr(self, name)
            if hasattr(attr, "__reacts_to__"):
                self.connection.dispatcher.register(attr.__reacts_to__, attr)

    def __del__(self) -> None:
        self.destroy()

    def destroy(self) -> None:
        """
        Destroy the reactor.

        This method is called when the reactor is detached from a connection.
        """
        for attr in self.__dict__.values():
            if hasattr(attr, "__reacts_to__"):
                self.connection.dispatcher.remove_handler(attr.__reacts_to__, attr)

    @property
    def client(self) -> Client:
        """
        The client that this reactor's connection is attached to.

        Returns
        -------
        :class:`Client`
        """
        return self.connection.client


REACTOR = TypeVar("REACTOR", bound=Reactor)
