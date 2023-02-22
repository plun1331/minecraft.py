"""
Copyright (c) 2023 plun1331

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from io import BytesIO
import json
from .base import Packet
from ..datatypes import *

class StatusResponse(Packet):
    """
    Status response packet sent by the server to the client in response to a status request.

    Packet ID: 0x00
    State: Status
    Bound to: Client
    """

    packet_id = 0x00

    def __init__(self, json_response: String):
        self.json_response = json_response

    @property
    def json(self):
        return json.loads(self.json_response)

    @classmethod
    def _from_bytes(cls, data: BytesIO):
        # Fields: json_response (string)
        # json_response
        json_response = String.from_bytes(data)
        return cls(json_response)

    def __repr__(self):
        return f"StatusResponse({self.json_response!r})"

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.json_response)
        )
    

class PingResponse(Packet):
    """
    Ping response packet sent by the server to the client in response to a ping request.

    Packet ID: 0x01
    State: Status
    Bound to: Client
    """

    packet_id = 0x01

    def __init__(self, payload: int):
        self.payload = payload

    @classmethod
    def _from_bytes(cls, data: BytesIO):
        # Fields: payload (long)
        # payload
        payload = Varint.from_bytes(data)
        return cls(payload)

    def __repr__(self):
        return f"PingResponse({self.payload!r})"

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") +
            self.payload.to_bytes(8, "big")
        )


class StatusRequest(Packet):
    """
    Status request packet sent by the client to the server to request the server's status.

    Packet ID: 0x00
    State: Status
    Bound to: Server
    """

    packet_id = 0x00

    def __init__(self):
        pass

    @classmethod
    def _from_bytes(cls, data: BytesIO):
        # Fields: None
        return cls()

    def __repr__(self):
        return "StatusRequest()"

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big")


class PingRequest(Packet):
    """
    Ping request packet sent by the client to the server to request the server's ping.

    Packet ID: 0x01
    State: Status
    Bound to: Server
    """

    packet_id = 0x01

    def __init__(self, payload: Long):
        self.payload: Long = payload

    @classmethod
    def _from_bytes(cls, data: BytesIO):
        # Fields: payload (long)
        # payload
        payload = Long.from_bytes(data)
        return cls(payload)

    def __repr__(self):
        return f"PingRequest({self.payload!r})"

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.payload)
        )