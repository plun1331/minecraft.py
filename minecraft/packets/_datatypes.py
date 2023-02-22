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


class Varint:
    """Variable length integer."""
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"Varint({self.value})"

    def __bytes__(self):
        value = self.value
        if value < 0:
            raise ValueError("Varint cannot be negative.")
        elif value == 0:
            return b"\x00"
        else:
            result = bytearray()
            while value > 0:
                temp = value & 0b01111111
                value >>= 7
                if value != 0:
                    temp |= 0b10000000
                result.append(temp)
            return bytes(result)

    @classmethod
    def from_bytes(cls, data: bytes):
        value = 0
        for i, byte in enumerate(data):
            value |= (byte & 0b01111111) << (7 * i)
            if not byte & 0b10000000:
                break
        return cls(value)

    @classmethod
    def size(cls, value: int):
        if value < 0:
            raise ValueError("Varint cannot be negative.")
        elif value == 0:
            return 1
        else:
            result = 0
            while value > 0:
                value >>= 7
                result += 1
            return result