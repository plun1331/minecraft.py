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

from .base import Packet
from ..datatypes import *
from ..enums import State


class StatusRequest(Packet):
    """
    Status request packet sent by the client to the server to request the server's status.

    **Packet ID**: ``0x00``

    **State**: :attr:`.State.STATUS`

    **Bound to**: Server
    """

    packet_id = 0x00
    bound_to = "server"
    state = State.STATUS

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: None
        return cls()

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big")


class PingRequest(Packet):
    """
    Ping request packet sent by the client to the server to request the server's ping.

    **Packet ID**: ``0x01``

    **State**: :attr:`.State.STATUS`

    **Bound to**: Server
    """

    packet_id = 0x01
    bound_to = "server"
    state = State.STATUS

    def __init__(self, payload: Long):
        self.payload: Long = payload

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: payload (long)
        # payload
        payload = Long.from_bytes(data)
        return cls(payload)

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.payload)
