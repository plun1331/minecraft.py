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

from io import BytesIO
from typing import Self


class Packet:
    """Represents a Minecraft packet."""

    packet_id: int = None

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls()

    @classmethod
    def decode(cls, data: bytes) -> Self:
        io = BytesIO(data)
        packet_id = int(io.read(1)[0])
        if packet_id != cls.packet_id:
            raise ValueError(
                f"Packet ID ({packet_id}) does not match expected packet ID ({cls.packet_id})"
            )
        return cls.from_bytes(io)

    def __repr__(self):
        return f"{self.__class__.__name__}(packet_id={self.packet_id})"

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big")

    def __len__(self):
        return len(self.packet_id.to_bytes(1, "big"))

    def __eq__(self, other):
        return bytes(self) == bytes(other)
