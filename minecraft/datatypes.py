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
from typing import Any
import uuid


class Boolean(int):
    """Boolean (1 byte)."""
    def __bytes__(self):
        return bytes([self])

    @classmethod
    def from_bytes(cls, data: BytesIO):
        return cls(data.read(1)[0])

    def size(self):
        return 1


class Byte(int):
    """Byte (1 byte)."""
    def __bytes__(self):
        return bytes([self])

    @classmethod
    def from_bytes(cls, data: BytesIO):
        return cls(data.read(1)[0])

    def size(self):
        return 1


class UnsignedByte(Byte):
    """Unsigned byte (1 byte)."""
    def __bytes__(self):
        return bytes([self])

    @classmethod
    def from_bytes(cls, data: BytesIO):
        return cls(data.read(1)[0])

    def size(self):
        return 1
    

class Short(int):
    """Short (2 bytes)."""
    def __bytes__(self):
        return bytes([self >> 8, self & 0xFF])

    @classmethod
    def from_bytes(cls, data: BytesIO):
        val = 0
        for i in range(2):
            val |= data.read(1)[0] << (8 * i)
        return cls(val)

    def size(self):
        return 2
    

class UnsignedShort(Short):
    """Unsigned short (2 bytes)."""
    

class Int(int):
    """Int (4 bytes)."""
    def __bytes__(self):
        arr = []
        for i in range(4):
            arr.append(self >> (8 * i) & 0xFF)
        return bytes(arr)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        val = 0
        for i in range(4):
            val |= data.read(1)[0] << (8 * i)
        return cls(val)

    def size(self):
        return 4


class Long(int):
    """Long (8 bytes)."""
    def __bytes__(self):
        arr = []
        for i in range(8):
            arr.append(self >> (8 * i) & 0xFF)
        return bytes(arr)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        val = 0
        for i in range(8):
            val |= data.read(1)[0] << (8 * i)
        return cls(val)

    def size(self):
        return 8
    

class Float(float):
    """Float (4 bytes)."""
    def __bytes__(self):
        return Int.from_bytes(self).to_bytes(4, "big")

    @classmethod
    def from_bytes(cls, data: BytesIO):
        return cls(Int.from_bytes(data))

    def size(self):
        return 4


class Double(float):
    """Double (8 bytes)."""
    def __bytes__(self):
        return Long.from_bytes(self).to_bytes(8, "big")

    @classmethod
    def from_bytes(cls, data: BytesIO):
        return cls(Long.from_bytes(data))

    def size(self):
        return 8
    

class String(str):
    """String with a Varint length prefix."""
    def __new__(cls, value: str):
        return super().__new__(cls, value)

    def __bytes__(self):
        return bytes(Varint(len(self))) + self.encode("utf-8")

    @classmethod
    def from_bytes(cls, data: BytesIO):
        string_length = Varint.from_bytes(data)
        return cls(data.read(string_length.value).decode("utf-8"))

    def size(self):
        return Varint.size(len(self)) + len(self)
    

class Chat(String):
    """Chat (String with max length of 262144)."""


class Identifier(String):
    """Identifier (String with max length of 32767)."""


class Varint(int):
    """Varint (1-5 bytes)."""
    def __new__(cls, value: int):
        return super().__new__(cls, value)

    def __bytes__(self):
        val = self.value
        arr = []
        while True:
            temp = val & 0b01111111
            val >>= 7
            if val != 0:
                temp |= 0b10000000
            arr.append(temp)
            if val == 0:
                break
        return bytes(arr)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        val = 0
        for i in range(5):
            temp = data.read(1)[0]
            val |= (temp & 0b01111111) << (7 * i)
            if not temp & 0b10000000:
                break
        return cls(val)

    def size(self):
        val = self.value
        size = 0
        while True:
            val >>= 7
            size += 1
            if val == 0:
                break
        return size
    

class Varlong(int):
    """Varlong (1-10 bytes)."""
    def __new__(cls, value: int):
        return super().__new__(cls, value)

    def __bytes__(self):
        val = self.value
        arr = []
        while True:
            temp = val & 0b01111111
            val >>= 7
            if val != 0:
                temp |= 0b10000000
            arr.append(temp)
            if val == 0:
                break
        return bytes(arr)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        val = 0
        for i in range(10):
            temp = data.read(1)[0]
            val |= (temp & 0b01111111) << (7 * i)
            if not temp & 0b10000000:
                break
        return cls(val)

    def size(self):
        val = self.value
        size = 0
        while True:
            val >>= 7
            size += 1
            if val == 0:
                break
        return size


class EntityMetadata:
    ...


class Slot:
    ...


class NBTTag:
    ...


class Position:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __bytes__(self):
        return (
            ((self.x & 0x3FFFFFF) << 38) | 
            ((self.z & 0x3FFFFFF) << 12) | 
            (self.y & 0xFFF)
        ).to_bytes(8, "big")

    @classmethod
    def from_bytes(cls, data: BytesIO):
        val = Long.from_bytes(data)
        x = val >> 38
        y = val << 52 >> 52
        z = val << 26 >> 38
        return cls(x, y, z)

    def size(self):
        return 8
    

class Angle:
    """A rotation angle in steps of 1/256 of a full turn (1 byte)."""
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self):
        return self.value.to_bytes(1, "big")

    @classmethod
    def from_bytes(cls, data: BytesIO):
        return cls(data.read(1)[0])

    def size(self):
        return 1
    

class UUID(int):
    """A UUID (16 bytes)."""
    def __new__(cls, value: int):
        return super().__new__(cls, value)

    def __bytes__(self):
        return self.value.to_bytes(16, "big")

    @classmethod
    def from_bytes(cls, data: BytesIO):
        return cls(Long.from_bytes(data))

    def size(self):
        return 16
    
    def __str__(self):
        return str(uuid.UUID(int=self.value))
    

class Optional:
    """Optional value (1 byte)."""
    def __init__(self, value: Any):
        self.value = value

    def __bytes__(self):
        return bytes(Varint(1 if self.value else 0)) + bytes(self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        return cls(Varint.from_bytes(data))

    def size(self):
        return Varint.size(1 if self.value else 0) + self.value.size()

    def __bool__(self):
        return bool(self.value)


class Array:
    """Array of values (Varint length prefix)."""
    def __init__(self, values: list[Any]):
        self.values = values

    def __bytes__(self):
        return bytes(Varint(len(self.values))) + b"".join(bytes(value) for value in self.values)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        length = Varint.from_bytes(data)
        return cls([data.read(length.value) for _ in range(length.value)])

    def size(self):
        return Varint.size(len(self.values)) + sum(value.size() for value in self.values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]

    def __setitem__(self, index, value):
        self.values[index] = value

    def __delitem__(self, index):
        del self.values[index]

    def __iter__(self):
        return iter(self.values)
    

class Enum:
    """Enum value (Varint)."""
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self):
        return bytes(Varint(self.value))

    @classmethod
    def from_bytes(cls, data: BytesIO):
        return cls(Varint.from_bytes(data))

    def size(self):
        return Varint.size(self.value)

    def __int__(self):
        return self.value
    

class ByteArray:
    """Byte array."""
    def __init__(self, value: bytearray):
        self.value = value

    def __bytes__(self):
        return bytes(Varint(len(self.value))) + bytes(self.value)
    
    @classmethod
    def from_bytes(cls, data: BytesIO, length: Varint | None = None):
        if length is None:
            return cls(data.read())
        return cls(data.read(length.value))
    
    def size(self):
        return len(self.value)

    @property
    def length(self):
        return Varint(len(self.value))


    


class Property:
    def __init__(self, name: String, value: String, signature: String | None = None):
        self.name = name
        self.value = value
        self.signature = signature

    @property
    def signed(self):
        return self.signature is not None
    
    def __bytes__(self):
        val = bytes(self.name) + bytes(self.value) + bytes(Boolean(self.signed))
        if self.signed:
            val += bytes(self.signature)
        return val
    
    @classmethod
    def from_bytes(cls, data: BytesIO):
        name = String.from_bytes(data)
        value = String.from_bytes(data)
        signed = Boolean.from_bytes(data)
        if signed:
            signature = String.from_bytes(data)
        else:
            signature = None
        return cls(name, value, signature)