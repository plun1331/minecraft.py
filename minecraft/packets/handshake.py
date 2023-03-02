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

#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#
#
#
from .base import Packet
from ..datatypes import *
from ..enums import NextState


class Handshake(Packet):
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
    def from_bytes(cls, data: BytesIO):
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

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.protocol_version)
            + bytes(self.server_address)
            + bytes(self.server_port)
            + bytes(self.next_state.value)
        )

    def __len__(self):
        return len(bytes(self))
