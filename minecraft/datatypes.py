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
import json
from io import BytesIO
from typing import Any
import uuid
import struct
from nbt import nbt

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class DataType:
    def __bytes__(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


class Boolean(DataType):
    def __init__(self, value: bool):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes([self.value])

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(bool(data.read(1)[0]))


class Byte(DataType):
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes([self.value])

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(data.read(1)[0])


class UnsignedByte(DataType):
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes([self.value])

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(data.read(1)[0])


class Short(DataType):
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">h", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">h", data.read(2))[0])


class UnsignedShort(DataType):
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">H", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">H", data.read(2))[0])


class Int(DataType):
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">i", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">i", data.read(4))[0])


class Long(DataType):
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">q", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">q", data.read(8))[0])


class Float(DataType):
    def __init__(self, value: float):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">f", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">f", data.read(4))[0])


class Double(DataType):
    def __init__(self, value: float):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">d", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">d", data.read(8))[0])


class String(DataType):
    def __init__(self, value: str):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes(UnsignedShort(len(self.value))) + self.value.encode("utf-8")

    @classmethod
    def from_bytes(cls, data: BytesIO, *, max_length: int = None) -> Self:
        length = UnsignedShort.from_bytes(data)
        if max_length is not None and length.value > (max_length * 4) + 3:
            raise ValueError(f"String length {length.value} exceeds max length {max_length}")
        return cls(data.read(length.value).decode("utf-8"))


class Chat(String):
    @property
    def json(self):
        return json.loads(self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return super().from_bytes(data, max_length=262144)


class Identifier(String):
    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return super().from_bytes(data, max_length=32767)


class Varint(DataType):
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        val = self.value
        out = bytearray()
        while True:
            temp = val & 0b01111111
            val >>= 7
            if val != 0:
                temp |= 0b10000000
            out.append(temp)
            if val == 0:
                break
        return bytes(out)

    @classmethod
    def from_bytes(cls, data: BytesIO, *, max_size: int = 5) -> Self:
        num_read = 0
        result = 0
        while True:
            read = data.read(1)[0]
            value = read & 0b01111111
            result |= value << (7 * num_read)

            num_read += 1
            if num_read > max_size:
                raise ValueError(f"Varint is too big (exceeded max size of {max_size} bytes)")

            if (read & 0b10000000) == 0:
                break

        return cls(result)


class Varlong(Varint):
    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return super().from_bytes(data, max_size=10)


"""
Entity Metadata is an array of entries, each of which looks like the following:

Name	Type	Meaning
Index	Unsigned Byte	Unique index key determining the meaning of the following value, see the table below. If this is 0xff then the it is the end of the Entity Metadata array and no more is read.
Type	Optional VarInt Enum	Only if Index is not 0xff; the type of the index, see the table below
Value	Optional value of Type	Only if Index is not 0xff: the value of the metadata field

Value of Type field	Type of Value field	Notes
0	Byte	
1	VarInt	
2	VarLong	
3	Float	
4	String	
5	Chat	
6	OptChat (Boolean + Optional Chat)	Chat is present if the Boolean is set to true
7	Slot	
8	Boolean	
9	Rotation	3 floats: rotation on x, rotation on y, rotation on z
10	Position	
11	OptPosition (Boolean + Optional Position)	Position is present if the Boolean is set to true
12	Direction (VarInt)	(Down = 0, Up = 1, North = 2, South = 3, West = 4, East = 5)
13	OptUUID (Boolean + Optional UUID)	UUID is present if the Boolean is set to true
14	OptBlockID (VarInt)	0 for absent (implies air); otherwise, a block state ID as per the global palette
15	NBT	
16	Particle	
17	Villager Data	3 VarInts: villager type, villager profession, level
18	OptVarInt	0 for absent; 1 + actual value otherwise. Used for entity IDs.
19	Pose	A VarInt enum: 0: STANDING, 1: FALL_FLYING, 2: SLEEPING, 3: SWIMMING, 4: SPIN_ATTACK, 5: SNEAKING, 6: LONG_JUMPING, 7: DYING, 8: CROAKING, 9: USING_TONGUE, 10: SITTING, 11: ROARING, 12: SNIFFING, 13: EMERGING, 14: DIGGING
20	Cat Variant	A VarInt that points towards the CAT_VARIANT registry.
21	Frog Variant	A VarInt that points towards the FROG_VARIANT registry.
22	GlobalPos	A dimension identifier and Position.
23	Painting Variant	A VarInt that points towards the PAINTING_VARIANT registry.
"""


class EntityMetadataEntry:
    def __init__(self, index: UnsignedByte, type: VarInt, value: DataType):
        self.index = index
        self.type = type
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes(self.index) + bytes(self.type) + bytes(self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO, index: UnsignedByte) -> Self:
        type = VarInt.from_bytes(data)
        value = {
            0: Byte.from_bytes,
            1: Varint.from_bytes,
            2: Varlong.from_bytes,
            3: Float.from_bytes,
            4: String.from_bytes,
            5: Chat.from_bytes,
            6: Chat.from_bytes,
            7: Slot.from_bytes,
            8: Boolean.from_bytes,
            9: Rotation.from_bytes,
            10: Position.from_bytes,
            11: Position.from_bytes,
            12: Varint.from_bytes,
            13: UUID.from_bytes,
            14: Varint.from_bytes,
            15: NBT.from_bytes,
            16: Particle.from_bytes,
            17: VillagerData.from_bytes,
            18: Varint.from_bytes,
            19: Varint.from_bytes,
            20: Varint.from_bytes,
            21: Varint.from_bytes,
            22: GlobalPos.from_bytes,
            23: Varint.from_bytes,
        }[type.value](data)
        return cls(index, type, value)


class Rotation(DataType):
    def __init__(self, x: Float, y: Float, z: Float):
        self.x = x
        self.y = y
        self.z = z

    def __bytes__(self) -> bytes:
        return bytes(self.x) + bytes(self.y) + bytes(self.z)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(Float.from_bytes(data), Float.from_bytes(data), Float.from_bytes(data))


class Particle(DataType):
    def __init__(self, name: Identifier, id: Varint, data: bytes):
        self.name: Identifier = name
        self.id: Varint = id
        self.data: bytes = data

    def __bytes__(self) -> bytes:
        return bytes(self.name) + bytes(self.id) + self.data

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(
            Identifier.from_bytes(data),
            Varint.from_bytes(data),
            data.read(),
        )


class VillagerData(DataType):
    def __init__(self, type: Varint, profession: Varint, level: Varint):
        self.type = type
        self.profession = profession
        self.level = level

    def __bytes__(self) -> bytes:
        return bytes(self.type) + bytes(self.profession) + bytes(self.level)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(
            Varint.from_bytes(data),
            Varint.from_bytes(data),
            Varint.from_bytes(data),
        )


class GlobalPos(DataType):
    def __init__(self, dimension: Identifier, position: 'Position'):
        self.dimension = dimension
        self.position = position

    def __bytes__(self) -> bytes:
        return bytes(self.dimension) + bytes(self.position)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(
            Identifier.from_bytes(data),
            Position.from_bytes(data),
        )


class EntityMetadata(DataType):
    def __init__(self, entries: list[EntityMetadataEntry]):
        self.entries = entries

    def __bytes__(self) -> bytes:
        out = bytearray()
        for entry in self.entries:
            out += bytes(entry)
        out += bytes(UnsignedByte(0xff))
        return bytes(out)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        entries = []
        while True:
            index = UnsignedByte.from_bytes(data)
            if index.value == 0xff:
                break
            entries.append(EntityMetadataEntry.from_bytes(data, index))
        return cls(entries)


class Slot(DataType):
    def __init__(self, present: Boolean, item: Item | None, count: UnsignedByte | None, nbt: NBT | None):
        self.present = present
        self.item = item
        self.count = count
        self.nbt = nbt

    def __bytes__(self) -> bytes:
        out = bytes(self.present)
        if self.present:
            out += bytes(self.item)
            out += bytes(self.count)
            out += bytes(self.nbt)
        return out

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        present = Boolean.from_bytes(data)
        if present:
            item_id = Varint.from_bytes(data)
            item_count = Byte.from_bytes(data)
            nbt = NBT.from_bytes(data)
        else:
            item = None
            count = None
            nbt = None
        return cls(present, item, count, nbt)


class NBT(DataType):
    def __init__(self, data: bytes):
        self.data = data

    @property
    def nbt(self):
        return nbt.NBTFile(buffer=BytesIO(self.data))

    def __bytes__(self) -> bytes:
        return bytes(Varint(len(self.data))) + self.data

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        length = Varint.from_bytes(data)
        return cls(data.read(length.value))


class Position(DataType):
    def __init__(self, x: Int, y: Int, z: Int):
        self.x = x
        self.y = y
        self.z = z

    def __bytes__(self) -> bytes:
        return bytes(
            ((self.x.value & 0x3FFFFFF) << 38) |
            ((self.z.value & 0x3FFFFFF) << 12) |
            (self.y.value & 0xFFF)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        val = Varlong.from_bytes(data)
        x = Int(val.value >> 38)
        y = Int(val.value << 52 >> 52)
        z = Int(val.value << 26 >> 38)
        return cls(x, y, z)


class Angle(DataType):
    def __init__(self, value: UnsignedByte):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes(self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(UnsignedByte.from_bytes(data))


class UUID(DataType):
    def __init__(self, most: Int, least: Int):
        self.most = most
        self.least = least

    @property
    def uuid(self):
        return uuid.UUID(bytes=bytes(self))

    def __bytes__(self) -> bytes:
        return bytes(self.most) + bytes(self.least)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        most = Int.from_bytes(data)
        least = Int.from_bytes(data)
        return cls(most, least)


class Array(DataType):
    def __init__(self, data_type: DataType, data: list[DataType]):
        self.data_type = data_type
        self.data = data

    def __bytes__(self) -> bytes:
        out = bytes(Varint(len(self.data)))
        for item in self.data:
            out += bytes(item)
        return out

    @classmethod
    def from_bytes(cls, data: BytesIO, length: int, *, x_type: Any) -> Self:
        out = []
        for _ in range(length):
            out.append(x_type.from_bytes(data))
        return cls(x_type, out)


class ByteArray(DataType):
    def __init__(self, data: bytes):
        self.data = data

    def __bytes__(self) -> bytes:
        return bytes(Varint(len(self.data))) + self.data

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        length = Varint.from_bytes(data)
        return cls(data.read(length.value))


class Property:
    def __init__(self, name: String, value: String, signature: String | None = None):
        self.name = name
        self.value = value
        self.signature = signature

    @property
    def signed(self):
        return self.signature is not None

    def __bytes__(self) -> bytes:
        val = bytes(self.name) + bytes(self.value) + bytes(Boolean(self.signed))
        if self.signed:
            val += bytes(self.signature)
        return val

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        name = String.from_bytes(data)
        value = String.from_bytes(data)
        signed = Boolean.from_bytes(data)
        if signed:
            signature = String.from_bytes(data)
        else:
            signature = None
        return cls(name, value, signature)
