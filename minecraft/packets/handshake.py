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

from enum import Enum
from .base import Packet
from ._datatypes import Varint


class NextState(Enum):
    STATUS = 1
    LOGIN = 2

class HandshakePacket(Packet):
    packet_id = 0x00

    def __init__(self, protocol_version: int, server_address: str, server_port: int, next_state: NextState):
        self.protocol_version = protocol_version
        self.server_address = server_address
        self.server_port = server_port
        self.next_state = next_state

    @classmethod
    def from_bytes(cls, data: bytes):
        packet_id = data[0]
        if packet_id != cls.packet_id:
            raise ValueError(f"Packet ID {packet_id} does not match expected packet ID {cls.packet_id}")
        # Fields: protocol_version (varint), server_address (string(255)), server_port (unsigned short), next_state (varint enum)
        protocol_version = Varint.from_bytes(data[1:]).value
        server_address = data[1 + len(Varint(protocol_version).to_bytes()):].split(b"\x00")[0].decode("utf-8")
        server_port = int.from_bytes(data[1 + len(Varint(protocol_version).to_bytes()) + len(server_address.encode("utf-8")) + len(b"\x00"):1 + len(Varint(protocol_version).to_bytes()) + len(server_address.encode("utf-8")) + len(b"\x00") + 2], "big")
        next_state = NextState(Varint.from_bytes(data[1 + len(Varint(protocol_version).to_bytes()) + len(server_address.encode("utf-8")) + len(b"\x00") + 2:]).value)
        return cls(protocol_version, server_address, server_port, next_state)

    def __repr__(self):
        return f"HandshakePacket({self.protocol_version}, {self.server_address}, {self.server_port}, {self.next_state})"

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + Varint(self.protocol_version).to_bytes() + self.server_address.encode("utf-8") + b"\x00" + self.server_port.to_bytes(2, "big") + Varint(self.next_state.value).to_bytes()

    def __len__(self):
        return len(bytes(self))
    
    def __eq__(self, other):
        return self.packet_id == other.packet_id and self.protocol_version == other.protocol_version and self.server_address == other.server_address and self.server_port == other.server_port and self.next_state == other.next_state