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

import json
from io import BytesIO

from .base import Packet
from ..datatypes import *
from ..enums import State


class StatusResponse(Packet):
    """
    Status response packet sent by the server to the client in response to a status request.

    **Packet ID**: ``0x00``

    **State**: :attr:`.State.STATUS`

    **Bound to**: Client
    """

    packet_id = 0x00
    bound_to = "client"
    state = State.STATUS

    def __init__(self, json_response: String):
        self.json_response = json_response

    @property
    def json(self):
        return json.loads(self.json_response.value)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: json_response (string)
        # json_response
        json_response = String.from_bytes(data)
        return cls(json_response)

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.json_response)


class PingResponse(Packet):
    """
    Ping response packet sent by the server to the client in response to a ping request.

    **Packet ID**: ``0x01``

    **State**: :attr:`.State.STATUS`

    **Bound to**: Client
    """

    packet_id = 0x01
    bound_to = "client"
    state = State.STATUS

    def __init__(self, payload: Varint):
        self.payload: Varint = payload

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: payload (long)
        # payload
        payload = Varint.from_bytes(data)
        return cls(payload)

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.payload)
