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
from .base import Packet
from ..datatypes import *
from ..enums import NextState


class HandshakePacket(Packet):
    """
    Handshake packet sent by the client to the server to initiate a connection.
    
    Packet ID: 0x00
    State: Handshaking
    Bound to: Server
    """
    packet_id = 0x00

    def __init__(
            self, 
            protocol_version: Varint, 
            server_address: String, 
            server_port: UnsignedShort, 
            next_state: NextState,
    ) -> None:
        self.protocol_version: Varint = protocol_version
        self.server_address: String = server_address
        self.server_port: UnsignedShort = server_port
        self.next_state: NextState = next_state

    @classmethod
    def _from_bytes(cls, data: BytesIO):
        # Fields: protocol_version (varint), server_address (string(255)), server_port (unsigned short), next_state (varint enum)
        # protocol version
        protocol_version = Varint.from_bytes(data)
        # server address
        server_address = String.from_bytes(data)
        # server port
        server_port = UnsignedShort.from_bytes(data)
        # next state
        next_state = NextState(Varint.from_bytes(data))
        return cls(protocol_version, server_address, server_port, next_state)

    def __repr__(self):
        return f"HandshakePacket({self.protocol_version}, {self.server_address}, {self.server_port}, {self.next_state})"

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") + 
            bytes(self.protocol_version) + 
            bytes(self.server_address) + 
            bytes(self.server_port) + 
            bytes(self.next_state.value)
        )
    
    def __len__(self):
        return len(bytes(self))
