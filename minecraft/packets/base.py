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

from io import BytesIO
from typing import Literal, Self

from ..enums import State


class Packet:
    """Represents a Minecraft packet."""

    packet_id: int = None  # :meta public:
    bound_to: Literal["client", "server"] = None  # :meta public:
    state: State = None  # :meta public:

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        """
        Converts a packet's data into a packet object.

        :param data: The packet's data.
        :type data: io.BytesIO

        :return: The packet object.
        :rtype: Packet
        """
        return cls()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(packet_id={self.packet_id} {' '.join([f'{k}={v}' for k, v in self.__dict__.items()])})"

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big")

    def __len__(self):
        return len(bytes(self))

    def __eq__(self, other):
        return bytes(self) == bytes(other)

    def __hash__(self):
        return hash(bytes(self))

    def to_bytes(self) -> bytes:
        return bytes(self)
