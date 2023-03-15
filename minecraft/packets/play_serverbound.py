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

from .base import Packet
from ..datatypes import *


class ConfirmTeleportation(Packet):
    """
    Sent by client as confirmation of Synchronize Player Position.

    Packet ID: 0x00
    State: Play
    Bound to: Server
    """

    packet_id = 0x00

    def __init__(self, teleport_id: Varint):
        self.teleport_id = teleport_id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.teleport_id)

    @classmethod
    def from_bytes(cls, data: bytes):
        # Fields: teleport_id (Varint)
        # teleport_id
        teleport_id = Varint.from_bytes(data[1:])
        return cls(teleport_id)


class QueryBlockEntityTag(Packet):
    """
    Used when ``Shift+F3+I`` is pressed while looking at a block.

    Packet ID: 0x01
    State: Play
    Bound to: Server
    """

    packet_id = 0x01

    def __init__(self, transaction_id: Varint, location: Position):
        self.transaction_id = transaction_id
        self.location = location

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.transaction_id)
            + bytes(self.location)
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        # Fields: transaction_id (Varint), location (Position)
        # transaction_id
        transaction_id = Varint.from_bytes(data[1:])
        # location
        location = Position.from_bytes(data[1 + len(transaction_id) :])
        return cls(transaction_id, location)


class ChangeDifficulty(Packet):
    """
    Only be used on singleplayer;
    the difficulty buttons are disabled in multiplayer.

    Packet ID: 0x02
    State: Play
    Bound to: Server
    """

    packet_id = 0x02

    def __init__(self, difficulty: UnsignedByte):
        self.difficulty = difficulty

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.difficulty)

    @classmethod
    def from_bytes(cls, data: bytes):
        # Fields: difficulty (UnsignedByte)
        # difficulty
        difficulty = UnsignedByte.from_bytes(data[1:])
        return cls(difficulty)
