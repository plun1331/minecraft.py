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
from typing_extensions import Self


class Packet:
    """Represents a Minecraft packet."""
    packet_id: int = None

    @classmethod()
    def from_bytes(cls, data: BytesIO) -> Self:
        raise NotImplementedError

    @classmethod
    def decode(cls, data: bytes) -> Self:
        io = BytesIO(data)
        packet_id = int(io.read(1)[0])
        if packet_id != cls.packet_id:
            raise ValueError(f"Packet ID ({packet_id}) does not match expected packet ID ({cls.packet_id})")
        return cls.from_bytes(io)

    def __repr__(self):
        return f"Packet({self.packet_id})"

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big")

    def __len__(self):
        return len(self.packet_id.to_bytes(1, "big"))

    def __eq__(self, other):
        return bytes(self) == bytes(other)
