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

from .datatypes import Chat


class DisconnectError(Exception):
    """
    Exception raised when the server disconnects the client.

    :ivar reason: The reason for the disconnect.
    :vartype reason: Chat
    """

    def __init__(self, reason):
        self.reason: Chat = reason

    def __str__(self):
        return str(self.reason)


class LoginDisconnectError(DisconnectError):
    """
    Exception raised when the server disconnects the client during the login phase.
    """

    pass


class MalformedPacketSizeError(Exception):
    """
    Exception raised when a packet that is too large is recieved.
    """

    pass


class UnknownPacketError(Exception):
    """
    Exception raised when a packet with an unknown ID is recieved.
    """

    def __init__(self, packet_id: int, data: bytes):
        super().__init__(f"Failed to find a packet with ID {packet_id}")
        self.packet_id: int = packet_id
        self.data: bytes = data


class PacketParsingError(Exception):
    """
    Exception raised when a packet fails to parse.

    :ivar original_exception: The original exception.
    :vartype original_exception: Exception
    :ivar packet_id: The packet ID.
    :vartype packet_id: int
    :ivar data: The packet data.
    :vartype data: bytes
    """
    def __init__(self, exc: Exception, packet_id: int, data: bytes) -> None:
        super().__init__(f"Failed to parse packet with ID {packet_id}: {exc}")
        self.original_exception: Exception = exc
        self.packet_id: int = packet_id
        self.data: bytes = data


class AuthenticationError(Exception):
    """
    Exception raised when the client fails to authenticate with the builtin Microsoft authentication scheme.

    :ivar message: The error message.
    :vartype message: str
    :ivar correlation_id: The correlation ID.
    :vartype correlation_id: str | None
    """

    def __init__(self, message: str, correlation_id: str | None = None) -> None:
        super().__init__(message)
        self.correlation_id = correlation_id
