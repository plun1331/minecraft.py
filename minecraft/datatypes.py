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

import json
import struct
import uuid
from io import BytesIO
from types import FrameType
from typing import Any, TYPE_CHECKING

from nbt import nbt

from .command_parsers import parsers as cmd_parsers

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

if TYPE_CHECKING:
    from .enums import StatCategory, StatID, CommandParser, MapIconType

__all__ = (
    "DataType",
    "Boolean",
    "Byte",
    "UnsignedByte",
    "Short",
    "UnsignedShort",
    "Int",
    "Long",
    "Float",
    "Double",
    "String",
    "Chat",
    "Identifier",
    "Varint",
    "Varlong",
    "Position",
    "Angle",
    "UUID",
    "NBT",
    "Slot",
    "ByteArray",
    "EntityMetadataEntry",
    "VillagerData",
    "EntityMetadata",
    "CommandNode",
    "CommandSuggestionMatch",
    "Statistic",
    "BlockEntity",
    "BitSet",
    "MapIcon",
    "Property",
    "Trade",
    "_DataProxy",
    "PlayerInfoUpdatePlayer",
    "Advancement",
    "AdvancementProgress",
    "CriterionProgress",
    "AdvancementDisplay",
    "Recipe",
    "ParticleType",
)


class DataType:
    """
    The base class for all data types.
    """
    def __bytes__(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        """
        Creates a new instance of this data type from the given bytes.

        :param data: The bytes to read from.
        :type data: io.BytesIO

        :return: The new instance.
        :rtype: DataType
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({' '.join([f'{k}={v}' for k, v in self.__dict__.items()])})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ != other.__dict__
        return False


class Boolean(DataType):
    """
    Represents a boolean value.

    :ivar value: The value of this data type.
    :vartype value: bool
    """
    def __init__(self, value: bool):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes([self.value])

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(bool(data.read(1)[0]))

    def __bool__(self):
        return self.value


class Byte(DataType):
    """
    Represents a byte.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes([self.value])

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(data.read(1)[0])


class UnsignedByte(DataType):
    """
    Represents an unsigned byte.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes([self.value])

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(data.read(1)[0])


class Short(DataType):
    """
    Represents a short.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">h", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">h", data.read(2))[0])


class UnsignedShort(DataType):
    """
    Represents an unsigned short.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">H", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">H", data.read(2))[0])


class Int(DataType):
    """
    Represents an integer.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">i", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">i", data.read(4))[0])


class Long(DataType):
    """
    Represents a long.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">q", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">q", data.read(8))[0])


class Float(DataType):
    """
    Represents a float.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: float):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">f", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">f", data.read(4))[0])


class Double(DataType):
    """
    Represents a double.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: float):
        self.value = value

    def __bytes__(self) -> bytes:
        return struct.pack(">d", self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(struct.unpack(">d", data.read(8))[0])


class String(DataType):
    """
    Represents a string.

    :ivar value: The value of this data type.
    :vartype value: str
    """
    def __init__(self, value: str):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes(Varint(len(self.value))) + self.value.encode("utf-8")

    @classmethod
    def from_bytes(cls, data: BytesIO, *, max_length: int = None) -> Self:
        length = Varint.from_bytes(data)
        if max_length is not None and length.value > (max_length * 4) + 3:
            raise ValueError(
                f"String length {length.value} exceeds max length {max_length}"
            )
        data = data.read(length.value)
        if len(data) != length.value:
            raise ValueError("String length mismatch")
        return cls(data.decode("utf-8"))


class Chat(String):
    """
    Represents chat data.

    :ivar value: The value of this data type.
    :vartype value: str
    """
    @property
    def json(self):
        """The parsed JSON data of this chat data. (:class:`dict`))"""
        return json.loads(self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return super().from_bytes(data, max_length=262144)


class Identifier(String):
    """
    Represents an identifier.

    :ivar value: The value of this data type.
    :vartype value: str
    """
    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return super().from_bytes(data, max_length=32767)


class Varint(DataType):
    """
    Represents a variable integer.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        value = self.value
        data = bytes()
        while True:
            if (value & ~0x7F) == 0:
                data += bytes([value])
                break
            data += bytes([(value & 0x7F) | 0x80])
            value >>= 7
        return bytes(data)

    @classmethod
    def from_bytes(cls, data: BytesIO, *, max_size: int = 5) -> Self:
        value = 0
        bits_read = 0

        while True:
            current_byte = data.read(1)[0]
            value |= (current_byte & 0x7F) << bits_read
            bits_read += 7

            if bits_read > 35:
                raise ValueError("Varint is too big")

            if (current_byte & 0x80) == 0:
                break

        if (value & 0x80000000) != 0:
            value = -((value ^ 0xFFFFFFFF) + 1)
        return cls(value)


class Varlong(DataType):
    """
    Represents a variable long.

    :ivar value: The value of this data type.
    :vartype value: int
    """
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        value = self.value
        data = bytes()
        while True:
            if (value & ~0x7F) == 0:
                data += bytes([value])
                break
            data += bytes([(value & 0x7F) | 0x80])
            value >>= 7
        return bytes(data)

    @classmethod
    def from_bytes(cls, data: BytesIO, *, max_size: int = 5) -> Self:
        value = 0
        bits_read = 0

        while True:
            current_byte = data.read(1)[0]
            value |= (current_byte & 0x7F) << bits_read
            bits_read += 7

            if bits_read > 64:
                raise Exception("Varlong is too big")

            if (current_byte & 0x80) == 0:
                break

        if (value & 0x8000000000000000) != 0:
            value = -((value ^ 0xFFFFFFFFFFFFFFFF) + 1)

        return cls(value)


class EntityMetadataEntry:
    """
    Represents entity metadata.

    :ivar index: The index key for this entry.
    :vartype index: UnsignedByte
    :ivar type: The type of index.
    :vartype type: Varint
    :ivar value: The value of this entry.
    :vartype value: DataType
    """
    def __init__(self, index: UnsignedByte, type: Varint, value: DataType):
        self.index = index
        self.type = type
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes(self.index) + bytes(self.type) + bytes(self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO, index: UnsignedByte) -> Self:
        type = Varint.from_bytes(data)
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
            16: ParticleType.from_bytes,
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
    """
    Represents the rotation of something.

    :ivar x: The x rotation.
    :vartype x: Float
    :ivar y: The y rotation.
    :vartype y: Float
    :ivar z: The z rotation.
    :vartype z: Float
    """
    def __init__(self, x: Float, y: Float, z: Float):
        self.x = x
        self.y = y
        self.z = z

    def __bytes__(self) -> bytes:
        return bytes(self.x) + bytes(self.y) + bytes(self.z)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(
            Float.from_bytes(data), Float.from_bytes(data), Float.from_bytes(data)
        )


class ParticleType(DataType):
    """
    Represents a particle.

    :ivar name: The name of this particle.
    :vartype name: Identifier
    :ivar id: The ID of this particle.
    :vartype id: Varint
    :ivar data: The particle's data.
    :vartype data: bytes
    """
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
    """
    Represents villager data.

    :ivar type: The type of villager.
    :vartype type: Varint
    :ivar profession: The profession of the villager.
    :vartype profession: Varint
    :ivar level: The level of the villager.
    :vartype level: Varint
    """
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
    """
    Represents a global position.
    
    :ivar dimension: The dimension of this position.
    :vartype dimension: Identifier
    :ivar position: The position in the dimension.
    :vartype position: Position"""
    def __init__(self, dimension: Identifier, position: "Position"):
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
    """
    Represents an entity's metadata.

    :ivar entries: The entries in this entity's metadata.
    :vartype entries: list[EntityMetadataEntry]
    """
    def __init__(self, entries: list[EntityMetadataEntry]):
        self.entries = entries

    def __bytes__(self) -> bytes:
        out = bytearray()
        for entry in self.entries:
            out += bytes(entry)
        out += bytes(UnsignedByte(0xFF))
        return bytes(out)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        entries = []
        while True:
            index = UnsignedByte.from_bytes(data)
            if index.value == 0xFF:
                break
            entries.append(EntityMetadataEntry.from_bytes(data, index))
        return cls(entries)


class NBT(DataType):
    """
    Represents NBT data.

    :ivar data: The raw NBT data.
    :vartype data: bytes
    """
    def __init__(self, data: bytes):
        self.data = data

    @property
    def nbt(self):
        """Parsed NBT data. (:class:`nbtlib.NBTFile`)"""
        return nbt.NBTFile(buffer=BytesIO(self.data))

    def __bytes__(self) -> bytes:
        return bytes(Varint(len(self.data))) + self.data

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        length = Varint.from_bytes(data)
        return cls(data.read(length.value))


class Slot(DataType):
    """
    Represents an item slot.

    :ivar present: Whether there is an item in this slot.
    :vartype present: Boolean
    :ivar item_id: The ID of the item in this slot.
    :vartype item_id: Varint | None
    :ivar count: The count of the item in this slot.
    :vartype count: UnsignedByte | None
    :ivar nbt: The NBT data of the item in this slot.
    :vartype nbt: NBT | None
    """
    def __init__(
        self,
        present: Boolean,
        item_id: Varint | None = None,
        count: UnsignedByte | None = None,
        _nbt: NBT | None = None,
    ):
        self.present = present
        self.item_id = item_id
        self.count = count
        self.nbt = _nbt

    def __bytes__(self) -> bytes:
        out = bytes(self.present)
        if self.present:
            out += bytes(self.item_id)
            out += bytes(self.count)
            out += bytes(self.nbt)
        return out

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        present = Boolean.from_bytes(data)
        if present:
            item_id = Varint.from_bytes(data)
            item_count = Byte.from_bytes(data)
            _nbt = NBT.from_bytes(data)
        else:
            item_id = None
            item_count = None
            _nbt = None
        return cls(present, item_id, item_count, _nbt)


class Position(DataType):
    """
    Represents a position in a world.

    :ivar x: The X coordinate of this position.
    :vartype x: Int
    :ivar y: The Y coordinate of this position.
    :vartype y: Int
    :ivar z: The Z coordinate of this position.
    :vartype z: Int
    """
    def __init__(self, x: Int, y: Int, z: Int):
        self.x = x
        self.y = y
        self.z = z

    def __bytes__(self) -> bytes:
        return bytes(
            ((self.x.value & 0x3FFFFFF) << 38)
            | ((self.z.value & 0x3FFFFFF) << 12)
            | (self.y.value & 0xFFF)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        val = Varlong.from_bytes(data)
        x = Int(val.value >> 38)
        y = Int(val.value << 52 >> 52)
        z = Int(val.value << 26 >> 38)
        return cls(x, y, z)


class Angle(DataType):
    """
    Represents an angle.
    
    :ivar value: The angle.
    :vartype value: UnsignedByte
    """
    def __init__(self, value: UnsignedByte):
        self.value = value

    def __bytes__(self) -> bytes:
        return bytes(self.value)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(UnsignedByte.from_bytes(data))


class Unsigned64Int(DataType):
    """
    Represents an unsigned 64-bit integer.

    :ivar value: The value of this unsigned 64-bit integer.
    :vartype value: int
    """
    # unsigned 64-bit integer
    def __init__(self, value: int):
        self.value = value

    def __bytes__(self) -> bytes:
        return self.value.to_bytes(8, "big")

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(int.from_bytes(data.read(8), "big"))


class UUID(DataType):
    """
    Represents a UUID. For a normal representation of this, see the :attr:`uuid` property.

    :ivar most: The most significant bits of this UUID.
    :vartype most: Unsigned64Int
    :ivar least: The least significant bits of this UUID.
    :vartype least: Unsigned64Int
    """
    def __init__(self, most: Unsigned64Int, least: Unsigned64Int):
        self.most = most
        self.least = least

    def __bytes__(self) -> bytes:
        return bytes(self.most) + bytes(self.least)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return cls(Unsigned64Int.from_bytes(data), Unsigned64Int.from_bytes(data))

    @property
    def uuid(self) -> uuid.UUID:
        """The parsed UUID. (:class:`uuid.UUID`)"""
        return uuid.UUID(int=(self.most.value << 64) | self.least.value)

    @classmethod
    def from_uuid(cls, uuid: uuid.UUID) -> Self:
        return cls(
            Unsigned64Int(uuid.int >> 64), Unsigned64Int(uuid.int & 0xFFFFFFFFFFFFFFFF)
        )

    @classmethod
    def from_string(cls, string: str) -> Self:
        return cls.from_uuid(uuid.UUID(string))


class Array(DataType):
    """
    Represents an array of data.

    :ivar data_type: The type of data in this array.
    :vartype data_type: DataType
    :ivar data: The data in this array. Type will be the same as :attr:`data_type`.
    :vartype data: list[DataType]
    """
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
    """
    Represents a byte array.

    :ivar data: The data in this byte array.
    :vartype data: bytes
    """
    def __init__(self, data: bytes):
        self.data = data

    def __bytes__(self) -> bytes:
        return self.data

    def __len__(self):
        return len(self.data)

    @classmethod
    def from_bytes(cls, data: BytesIO, *, length: int = None) -> Self:
        if length is None:
            return cls(data.read())
        return cls(data.read(length))


class Property(DataType):
    """
    Represents a property.

    :ivar name: The name of this property.
    :vartype name: String
    :ivar value: The value of this property.
    :vartype value: String
    :ivar signature: The signature of this property.
    :vartype signature: String | None
    """
    def __init__(self, name: String, value: String, signature: String | None = None):
        self.name = name
        self.value = value
        self.signature = signature

    def __bytes__(self) -> bytes:
        val = bytes(self.name) + bytes(self.value) + bytes(Boolean(self.signed))
        if self.signature is not None:
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


class Statistic(DataType):
    """
    Represents a statistic.

    :ivar category: The category of this statistic.
    :vartype category: StatCategory
    :ivar stat_id: The ID of this statistic.
    :vartype stat_id: StatID
    :ivar value: The value of this statistic.
    :vartype value: Varint
    """
    def __init__(self, category: StatCategory, stat_id: StatID, value: Varint):
        self.category: StatCategory = category
        self.stat_id: StatID = stat_id
        self.value: Varint = value

    def __bytes__(self) -> bytes:
        return (
            bytes(self.category.value) + bytes(self.stat_id.value) + bytes(self.value)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        from .enums import StatCategory, StatID

        category = StatCategory.from_value(Varint.from_bytes(data))
        stat_id = StatID.from_value(Varint.from_bytes(data))
        value = Varint.from_bytes(data)
        return cls(category, stat_id, value)


class CommandSuggestionMatch(DataType):
    """
    Represents a command suggestion match.

    :ivar match: The match.
    :vartype match: String
    :ivar tooltip: The tooltip.
    :vartype tooltip: Chat | None
    """
    def __init__(self, match: String, tooltip: Chat | None = None):
        self.match: String = match
        self.tooltip: Chat | None = tooltip

    def __bytes__(self) -> bytes:
        return (
            bytes(self.match) + bytes(Boolean(self.tooltip is not None)) + (
            bytes(self.tooltip) if self.tooltip is not None else b""
            )
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        match = String.from_bytes(data)
        has_tooltip = Boolean.from_bytes(data)
        if has_tooltip:
            tooltip = Chat.from_bytes(data)
        else:
            tooltip = None
        return cls(match, tooltip)


class CommandNode(DataType):
    """
    Represents a command node.

    :ivar flags: The flags of this command node.
    :vartype flags: Byte
    :ivar children: The children of this command node.
    :vartype children: list[Varint]
    :ivar redirect: The redirect of this command node.
    :vartype redirect: Varint | None
    :ivar name: The name of this command node.
    :vartype name: String | None
    :ivar parser: The parser of this command node.
    :vartype parser: CommandParser | None
    :ivar properties: The properties of this command node.
    :vartype properties: bytes | None
    :ivar suggestions_type: The suggestions type of this command node.
    :vartype suggestions_type: Identifier | None
    """
    def __init__(
        self,
        flags: Byte,
        children: list[Varint],
        redirect: Varint | None = None,
        name: String | None = None,
        parser: CommandParser | None = None,
        properties: bytes | None = None,
        suggestions_type: Identifier | None = None,
    ):
        self.flags: Byte = flags
        self.children: list[Varint] = children
        self.redirect: Varint | None = redirect
        self.name: String | None = name
        self.parser: CommandParser | None = parser
        self.properties: bytes | None = properties
        self.suggestions: Identifier | None = suggestions_type

    def __bytes__(self) -> bytes:
        return (
            bytes(self.flags)
            + bytes(Varint(len(self.children)))
            + b"".join(bytes(child) for child in self.children)
            + (bytes(self.redirect) if self.flags.value & 0x08 else b"")
            + (bytes(self.name) if self.flags.value & 0x03 != 0 else b"")
            + (bytes(self.parser.value) if self.flags.value & 0x03 == 2 else b"")
            + (  # type: ignore
                bytes(self.properties) if self.flags.value & 0x03 == 2 else b""
            )
            + (bytes(self.suggestions) if self.flags.value & 0x10 else b"")
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        from .enums import CommandParser

        flags = Byte.from_bytes(data)
        children = []
        children_count = Varint.from_bytes(data)
        for _ in range(children_count.value):
            children.append(Varint.from_bytes(data))
        _flags = flags.value
        redirect = Varint.from_bytes(data) if _flags & 0x08 else None
        name = String.from_bytes(data) if _flags & 0x03 != 0 else None
        parser = CommandParser(Varint.from_bytes(data)) if _flags & 0x03 == 2 else None
        properties = None
        if parser and parser.value.value in cmd_parsers:
            properties = cmd_parsers[parser.value.value].from_bytes(data)
        suggestions = Identifier.from_bytes(data) if _flags & 0x10 else None
        return cls(flags, children, redirect, name, parser, properties, suggestions)

    def __repr__(self):
        return (
            f"CommandNode({self.flags}, {self.children}, {self.redirect}, "
            f"{self.name}, {self.parser}, {self.properties}, {self.suggestions})"
        )


class BlockEntity(DataType):
    """
    Represents a block entity.

    :ivar xz: The x and z coordinates of this block entity.
    :vartype xz: Byte
    :ivar y: The y coordinate of this block entity.
    :vartype y: Short
    :ivar type: The type of this block entity.
    :vartype type: Varint
    :ivar data: The data of this block entity.
    :vartype data: NBT
    """
    def __init__(self, xz: Byte, y: Short, type: Varint, data: NBT):
        self.xz: Byte = xz
        self.y: Short = y
        self.type: Varint = type
        self.data: NBT = data

    @property
    def x(self):
        """The x coordinate of this block entity. (:class:`int`)"""
        return self.xz.value >> 4

    @property
    def z(self):
        """The z coordinate of this block entity. (:class:`int`)"""
        return self.xz.value & 15

    def __bytes__(self) -> bytes:
        return bytes(self.xz) + bytes(self.y) + bytes(self.type) + bytes(self.data)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        xz = Byte.from_bytes(data)
        y = Short.from_bytes(data)
        type = Varint.from_bytes(data)
        data = NBT.from_bytes(data)
        return cls(xz, y, type, data)


class BitSet(DataType):
    """
    Represents a bit set.
    
    :ivar longs: The longs of this bit set.
    :vartype longs: list[Long]
    """
    def __init__(self, longs: list[Long]):
        self.longs: list[Long] = longs

    def __bytes__(self) -> bytes:
        return bytes(Varint(len(self.longs))) + b"".join(
            bytes(long) for long in self.longs
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        longs = []
        longs_count = Varint.from_bytes(data)
        for _ in range(longs_count.value):
            longs.append(Long.from_bytes(data))
        return cls(longs)

    def __repr__(self):
        return f"BitSet({self.longs})"


class MapIcon(DataType):
    """
    Represents a map icon.
    
    :ivar type: The type of this map icon.
    :vartype type: MapIconType
    :ivar x: The x coordinate of this map icon.
    :vartype x: Byte
    :ivar y: The y coordinate of this map icon.
    :vartype y: Byte
    :ivar direction: The direction this icon is pointing.
    :vartype direction: Byte
    :ivar display_name: The display name of this map icon.
    :vartype display_name: Chat
    """
    def __init__(
        self,
        type: MapIconType,
        x: Byte,
        y: Byte,
        direction: Byte,
        display_name: Chat | None,
    ):
        self.type: MapIconType = type
        self.x: Byte = x
        self.y: Byte = y
        self.direction: Byte = direction
        self.display_name: Chat | None = display_name

    def __bytes__(self) -> bytes:
        return (
            bytes(self.type.value)
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.direction)
            + bytes(Boolean(self.display_name is not None))
            + bytes(self.display_name)
            if self.display_name
            else b""
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        from .enums import MapIconType

        type = MapIconType(Byte.from_bytes(data))
        x = Byte.from_bytes(data)
        y = Byte.from_bytes(data)
        direction = Byte.from_bytes(data)
        has_display_name = Boolean.from_bytes(data)
        display_name = Chat.from_bytes(data) if has_display_name else None
        return cls(type, x, y, direction, display_name)


class Trade(DataType):
    """
    Represents a villager trade.

    :ivar input_item_1: The first input item of this trade.
    :vartype input_item_1: Slot
    :ivar output_item: The output item of this trade.
    :vartype output_item: Slot
    :ivar input_item_2: The second input item of this trade.
    :vartype input_item_2: Slot
    :ivar trade_disabled: Whether this trade is disabled.
    :vartype trade_disabled: Boolean
    :ivar trade_uses: The number of times this trade has been used.
    :vartype trade_uses: Int
    :ivar max_trade_uses: The maximum number of times this trade can be used.
    :vartype max_trade_uses: Int
    :ivar xp: The amount of experience this trade gives.
    :vartype xp: Int
    :ivar special_price: The special price of this trade.
    :vartype special_price: Int
    :ivar price_multiplier: The price multiplier of this trade.
    :vartype price_multiplier: Float
    :ivar demand: The demand of this trade.
    :vartype demand: Int
    """
    def __init__(
        self,
        input_item_1: Slot,
        output_item: Slot,
        input_item_2: Slot,
        trade_disabled: Boolean,
        trade_uses: Int,
        max_trade_uses: Int,
        xp: Int,
        special_price: Int,
        price_multiplier: Float,
        demand: Int,
    ):
        self.input_item_1: Slot = input_item_1
        self.output_item: Slot = output_item
        self.input_item_2: Slot = input_item_2
        self.trade_disabled: Boolean = trade_disabled
        self.trade_uses: Int = trade_uses
        self.max_trade_uses: Int = max_trade_uses
        self.xp: Int = xp
        self.special_price: Int = special_price
        self.price_multiplier: Float = price_multiplier
        self.demand: Int = demand

    def __bytes__(self) -> bytes:
        return (
            bytes(self.input_item_1)
            + bytes(self.output_item)
            + bytes(self.input_item_2)
            + bytes(self.trade_disabled)
            + bytes(self.trade_uses)
            + bytes(self.max_trade_uses)
            + bytes(self.xp)
            + bytes(self.special_price)
            + bytes(self.price_multiplier)
            + bytes(self.demand)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        input_item_1 = Slot.from_bytes(data)
        output_item = Slot.from_bytes(data)
        input_item_2 = Slot.from_bytes(data)
        trade_disabled = Boolean.from_bytes(data)
        trade_uses = Int.from_bytes(data)
        max_trade_uses = Int.from_bytes(data)
        xp = Int.from_bytes(data)
        special_price = Int.from_bytes(data)
        price_multiplier = Float.from_bytes(data)
        demand = Int.from_bytes(data)
        return cls(
            input_item_1,
            output_item,
            input_item_2,
            trade_disabled,
            trade_uses,
            max_trade_uses,
            xp,
            special_price,
            price_multiplier,
            demand,
        )


class _DataProxy:
    """
    A proxy class for data types that do not have their own class.

    All attributes on this class are dynamic.

    :meta public:
    """
    def __init__(self, **attrs):
        self.attrs = {k: v for k, v in attrs.items() if k != "attrs"}

    def __getattr__(self, name):
        return self.attrs[name]

    def __setattr__(self, name, value):
        if name == "attrs":
            return super().__setattr__(name, value)
        self.attrs[name] = value

    def __repr__(self):
        return f"_DataProxy({', '.join(f'{k}={v!r}' for k, v in self.attrs.items())})"


class PlayerInfoUpdatePlayer(DataType):
    """
    Represents a player info update for a single player.

    :ivar uuid: The UUID of the player.
    :vartype uuid: UUID
    :ivar add_player: The add player data.
    :vartype add_player: _DataProxy
    :ivar initialize_chat: The initialize chat data.
    :vartype initialize_chat: _DataProxy
    :ivar update_gamemode: The update gamemode data.
    :vartype update_gamemode: _DataProxy
    :ivar update_listed: The update listed data.
    :vartype update_listed: _DataProxy
    :ivar update_latency: The update latency data.
    :vartype update_latency: _DataProxy
    :ivar update_display_name: The update display name data.
    :vartype update_display_name: _DataProxy

    **Data Proxy Attributes**

    * :attr:`add_player`:
        * **name**( :class:`String`) - The name of the player. 
        * **properties** (list[:class:`Property`]) - The properties of the player. 
    * :attr:`initialize_chat`:
        * **has_signature_data** (:class:`Boolean`) - Whether the object has signature data. Other attributes will be ``None`` if this is ``False``. 
        * **chat_session_id** (:class:`UUID` | None) - The chat session ID.
        * **public_key_expiry** (:class:`Long` | None) - The public key expiry.
        * **public_key** (:class:`ByteArray` | None) - The public key.
        * **public_key_signature** (:class:`ByteArray` | None) - The signature.
    * :attr:`update_gamemode`:
        * **gamemode** (:class:`VarInt`) - The gamemode of the player.
    * :attr:`update_listed`:
        * **listed** (:class:`Boolean`) - Whether the player is listed.
    * :attr:`update_latency`:
        * **latency** (:class:`VarInt`) - The latency of the player. 
    * :attr:`update_display_name`:
        * **has_display_name** (:class:`Boolean`) - Whether the player has a display name. 
        * **display_name** (:class:`String` | None) - The display name of the player. ``None`` if ``has_display_name`` is ``False``. 
    
    """
    def __init__(
        self,
        uuid: UUID,
        add_player: _DataProxy | None = None,
        initialize_chat: _DataProxy | None = None,
        update_gamemode: _DataProxy | None = None,
        update_listed: _DataProxy | None = None,
        update_latency: _DataProxy | None = None,
        update_display_name: _DataProxy | None = None,
    ):
        self.uuid: UUID = uuid
        self.add_player: _DataProxy | None = add_player
        self.initialize_chat: _DataProxy | None = initialize_chat
        self.update_gamemode: _DataProxy | None = update_gamemode
        self.update_listed: _DataProxy | None = update_listed
        self.update_latency: _DataProxy | None = update_latency
        self.update_display_name: _DataProxy | None = update_display_name

    def __bytes__(self) -> bytes:
        res = bytes(self.uuid)
        if self.add_player:
            res += bytes(self.add_player.name)
            res += bytes(Varint(len(self.add_player.properties)))
            for property in self.add_player.properties:
                res += bytes(property)
        if self.initialize_chat:
            res += bytes(self.initialize_chat.has_signature_data)
            if self.initialize_chat.has_signature_data:
                res += bytes(self.initialize_chat.chat_session_id)
                res += bytes(self.initialize_chat.public_key_expiry)
                res += bytes(Varint(len(self.initialize_chat.public_key)))
                res += bytes(self.initialize_chat.public_key)
                res += bytes(Varint(len(self.initialize_chat.public_key_signature)))
                res += bytes(self.initialize_chat.public_key_signature)
        if self.update_gamemode:
            res += bytes(self.update_gamemode.gamemode)
        if self.update_listed:
            res += bytes(self.update_listed.listed)
        if self.update_latency:
            res += bytes(self.update_latency.latency)
        if self.update_display_name:
            res += bytes(Boolean(self.update_display_name.display_name is not None))
            if self.update_display_name.display_name is not None:
                res += bytes(self.update_display_name.display_name)
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO, actions: Byte) -> Self:
        from .enums import PlayerInfoUpdateActionBits

        uuid = UUID.from_bytes(data)
        add_player = None
        initialize_chat = None
        update_gamemode = None
        update_listed = None
        update_latency = None
        update_display_name = None
        if actions.value & PlayerInfoUpdateActionBits.ADD_PLAYER.value:
            name = String.from_bytes(data)
            properties_count = Varint.from_bytes(data).value
            properties = []
            for _ in range(properties_count):
                properties.append(Property.from_bytes(data))
            add_player = _DataProxy(
                name=name,
                properties=properties,
            )
        if actions.value & PlayerInfoUpdateActionBits.INITIALIZE_CHAT.value:
            has_signature_data = Boolean.from_bytes(data)
            chat_session_id = None
            public_key_expiry = None
            public_key = None
            public_key_signature = None
            if has_signature_data:
                chat_session_id = UUID.from_bytes(data)
                public_key_expiry = Long.from_bytes(data)
                pk_size = Varint.from_bytes(data).value
                public_key = ByteArray.from_bytes(data, length=pk_size)
                pk_sig_size = Varint.from_bytes(data).value
                public_key_signature = ByteArray.from_bytes(data, length=pk_sig_size)
            initialize_chat = _DataProxy(
                has_signature_data=has_signature_data,
                chat_session_id=chat_session_id,
                public_key_expiry=public_key_expiry,
                public_key=public_key,
                public_key_signature=public_key_signature,
            )
        if actions.value & PlayerInfoUpdateActionBits.UPDATE_GAMEMODE.value:
            gamemode = Varint.from_bytes(data)
            update_gamemode = _DataProxy(
                gamemode=gamemode,
            )
        if actions.value & PlayerInfoUpdateActionBits.UPDATE_LISTED.value:
            listed = Boolean.from_bytes(data)
            update_listed = _DataProxy(
                listed=listed,
            )
        if actions.value & PlayerInfoUpdateActionBits.UPDATE_LATENCY.value:
            latency = Varint.from_bytes(data)
            update_latency = _DataProxy(
                latency=latency,
            )
        if actions.value & PlayerInfoUpdateActionBits.UPDATE_DISPLAY_NAME.value:
            has_display_name = Boolean.from_bytes(data)
            display_name = None
            if has_display_name:
                display_name = Chat.from_bytes(data)
            update_display_name = _DataProxy(
                has_display_name=has_display_name,
                display_name=display_name,
            )
        return cls(
            uuid,
            add_player,
            initialize_chat,
            update_gamemode,
            update_listed,
            update_latency,
            update_display_name,
        )


class Advancement(DataType):
    """
    Represents an advancement.
    
    :ivar parent_id: The advancement's parent ID.
    :vartype parent_id: String | None
    :ivar display_data: The advancement's display data.
    :vartype display_data: _DataProxy | None
    :ivar criteria: The advancement's criteria.
    :vartype criteria: dict[Identifier, None]
    :ivar requirements: The advancement's requirements.
    :vartype requirements: list[list[String]]
    """
    def __init__(
        self,
        parent_id: String | None = None,
        display_data: _DataProxy | None = None,
        criteria: dict[Identifier, None] | None = None,
        requirements: list[list[String]] | None = None,
    ):
        self.parent_id: String | None = parent_id
        self.display_data: _DataProxy | None = display_data
        self.criteria: dict[Identifier, None] = criteria or {}
        self.requirements: list[list[String]] = requirements or []

    def __bytes__(self) -> bytes:
        res = bytes(Boolean(self.parent_id is not None))
        if self.parent_id is not None:
            res += bytes(String(self.parent_id))
        res += bytes(Boolean(self.display_data is not None))
        if self.display_data is not None:
            res += bytes(self.display_data)
        res += bytes(Varint(len(self.criteria)))
        for criteria in self.criteria:
            res += bytes(String(criteria))
        res += bytes(Varint(len(self.requirements)))
        for requirement in self.requirements:
            res += bytes(Varint(len(requirement)))
            for requirement_item in requirement:
                res += bytes(requirement_item)
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        parent_id = None
        if Boolean.from_bytes(data):
            parent_id = String.from_bytes(data)
        display_data = None
        if Boolean.from_bytes(data):
            display_data = _DataProxy.from_bytes(data)
        criteria_count = Varint.from_bytes(data).value
        criteria = {}
        for _ in range(criteria_count):
            criteria[String.from_bytes(data)] = None
        requirements_count = Varint.from_bytes(data).value
        requirements = []
        for _ in range(requirements_count):
            requirement_count = Varint.from_bytes(data).value
            requirement = []
            for _ in range(requirement_count):
                requirement.append(String.from_bytes(data))
            requirements.append(requirement)
        return cls(
            parent_id,
            display_data,
            criteria,
            requirements,
        )


class AdvancementDisplay(DataType):
    """
    Represents an advancement display.  
    
    :ivar title: The advancement's title.
    :vartype title: Chat
    :ivar description: The advancement's description.
    :vartype description: Chat
    :ivar icon: The advancement's icon.
    :vartype icon: Identifier
    :ivar frame_type: The advancement's frame type.
    :vartype frame_type: FrameType
    :ivar flags: The advancement's flags.
    :vartype flags: Int
    :ivar background_texture: The advancement's background texture.
    :vartype background_texture: Identifier | None
    :ivar x: The advancement's X position.
    :vartype x: float
    :ivar y: The advancement's Y position.
    :vartype y: float
    """
    def __init__(
        self,
        title: Chat,
        description: Chat,
        icon: Identifier,
        frame_type: FrameType,
        flags: Int,
        background_texture: Identifier | None,
        x: Float,
        y: Float,
    ):
        self.title: Chat = title
        self.description: Chat = description
        self.icon: Slot = icon
        self.frame_type: FrameType = frame_type
        self.flags: int = flags
        self.background_texture: Identifier | None = background_texture
        self.x: Float = x
        self.y: Float = y

    def __bytes__(self) -> bytes:
        res = bytes(self.title)
        res += bytes(self.description)
        res += bytes(self.icon)
        res += bytes(Varint(self.frame_type.value))
        res += bytes(Varint(self.flags))
        if self.flags.value & 0x01:
            res += bytes(self.background_texture)
        res += bytes(Float(self.x))
        res += bytes(Float(self.y))
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        title = Chat.from_bytes(data)
        description = Chat.from_bytes(data)
        icon = Slot.from_bytes(data)
        frame_type = FrameType(Varint.from_bytes(data).value)
        flags = Varint.from_bytes(data).value
        background_texture = None
        if flags.value & 0x01:
            background_texture = Identifier.from_bytes(data)
        x = Float.from_bytes(data)
        y = Float.from_bytes(data)
        return cls(
            title,
            description,
            icon,
            frame_type,
            flags,
            background_texture,
            x,
            y,
        )


class CriterionProgress(DataType):
    """
    Represents progress for a criterion.

    :ivar achieved: Whether the criterion has been achieved.
    :vartype achieved: Boolean
    :ivar date: The date the criterion was achieved.
    :vartype date: Long | None
    """
    def __init__(
        self,
        achieved: Boolean,
        date: Long | None = None,
    ):
        self.achieved: Boolean = achieved
        self.date: Long | None = date

    def __bytes__(self) -> bytes:
        res = bytes(self.achieved)
        if self.achieved:
            res += bytes(self.date)
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        achieved = Boolean.from_bytes(data)
        date = None
        if achieved:
            date = Long.from_bytes(data)
        return cls(
            achieved,
            date,
        )


class AdvancementProgress(DataType):
    """
    Represents progress towards an advancement.

    :ivar identifier: The advancement's identifier.
    :vartype identifier: Identifier
    :ivar progress: The advancement's progress.
    :vartype progress: CriterionProgress
    """
    def __init__(
        self,
        identifier: Identifier,
        progress: CriterionProgress,
    ):
        self.identifier: Identifier = identifier
        self.progress: CriterionProgress = progress

    def __bytes__(self) -> bytes:
        res = bytes(self.identifier)
        res += bytes(self.progress)
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        identifier = Identifier.from_bytes(data)
        progress = CriterionProgress.from_bytes(data)
        return cls(
            identifier,
            progress,
        )


class Ingredient(DataType):
    """
    Represents an ingredient in a crafting recipe.
    
    :ivar items: The ingredient's items.
    :vartype items: list[Slot]
    """
    def __init__(
        self,
        items: list[Slot],
    ):
        self.items: list[Slot] = items

    def __bytes__(self) -> bytes:
        res = bytes(Varint(len(self.items)))
        for item in self.items:
            res += bytes(item)
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        items_count = Varint.from_bytes(data).value
        items = []
        for _ in range(items_count):
            items.append(Slot.from_bytes(data))
        return cls(
            items,
        )


class Recipe(DataType):
    """
    Represents a recipe.

    :ivar recipe_type: The recipe type.
    :vartype recipe_type: Identifier
    :ivar recipe_id: The recipe ID.
    :vartype recipe_id: Identifier
    :ivar data: The recipe data.
    :vartype data: _DataProxy

    .. admonition:: TODO
        :class: note

        Add recipe types and their respective data proxy values.
    """
    def __init__(
        self,
        recipe_type: Identifier,
        recipe_id: Identifier,
        data: _DataProxy,
    ):
        self.recipe_type: Identifier = recipe_type
        self.recipe_id: Identifier = recipe_id
        self.data: _DataProxy = data

    def __bytes__(self) -> bytes:
        res = bytes(self.recipe_type)
        res += bytes(self.recipe_id)
        if self.recipe_type.value == "minecraft:crafting_shapeless":
            res += bytes(self.data.group)
            res += bytes(Varint(self.data.category))
            res += bytes(Varint(len(self.data.ingredients)))
            for ingredient in self.data.ingredients:
                res += bytes(ingredient)
            res += bytes(self.data.result)
        elif self.recipe_type.value == "minecraft:crafting_shaped":
            res += bytes(Varint(self.data.width))
            res += bytes(Varint(self.data.height))
            res += bytes(self.data.group)
            res += bytes(Varint(self.data.category))
            for ingredient in self.data.ingredients:
                res += bytes(ingredient)
            res += bytes(self.data.result)
            res += bytes(self.data.show_notification)
        elif (
            self.recipe_type.value.startswith("minecraft:crafting_special_")
            or self.recipe_type.value == "minecraft:crafting_decorated_pot"
        ):
            res += bytes(Varint(self.data.category))
        elif self.recipe_type.value in (
            "minecraft:smelting",
            "minecraft:blasting",
            "minecraft:smoking",
            "minecraft:campfire_cooking",
            "minecraft:stonecutting",
        ):
            res += bytes(self.data.group)
            res += bytes(Varint(self.data.category))
            res += bytes(self.data.ingredient)
            res += bytes(self.data.result)
            res += bytes(Float(self.data.experience))
            res += bytes(Varint(self.data.cooking_time))
        elif self.recipe_type.value == "minecraft:stonecutting":
            res += bytes(self.data.group)
            res += bytes(Varint(self.data.category))
            res += bytes(self.data.ingredient)
            res += bytes(self.data.result)
        elif self.recipe_type.value == "minecraft:smithing":
            res += bytes(self.data.base)
            res += bytes(self.data.addition)
            res += bytes(self.data.result)
        elif self.recipe_type.value == "minecraft:smithing_transform":
            res += bytes(self.data.template)
            res += bytes(self.data.base)
            res += bytes(self.data.addition)
            res += bytes(self.data.result)
        elif self.recipe_type.value == "minecraft:smithing_trim":
            res += bytes(self.data.template)
            res += bytes(self.data.base)
            res += bytes(self.data.addition)
        else:
            raise ValueError(f"Unknown recipe type {self.recipe_type}")
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        try:
            recipe_type = Identifier.from_bytes(data)
        except (ValueError, IndexError):
            recipe_type = None
        try:
            recipe_id = Identifier.from_bytes(data)
        except (ValueError, IndexError):
            recipe_id = None
        _data = None
        if recipe_type:
            if recipe_type.value == "minecraft:crafting_shapeless":
                _data = _DataProxy(
                    group=String.from_bytes(data),
                    category=Varint.from_bytes(data),
                    ingredients=[
                        Ingredient.from_bytes(data)
                        for _ in range(Varint.from_bytes(data).value)
                    ],
                    result=Slot.from_bytes(data),
                )
            elif recipe_type.value == "minecraft:crafting_shaped":
                width = Varint.from_bytes(data).value
                height = Varint.from_bytes(data).value
                _data = _DataProxy(
                    width=width,
                    height=height,
                    group=String.from_bytes(data),
                    category=Varint.from_bytes(data),
                    ingredients=[
                        Ingredient.from_bytes(data) for _ in range(width * height)
                    ],
                    result=Slot.from_bytes(data),
                    show_notification=Boolean.from_bytes(data),
                )
            elif (
                recipe_type.value.startswith("minecraft:crafting_special_")
                or recipe_type.value == "minecraft:crafting_decorated_pot"
            ):
                _data = _DataProxy(
                    category=Varint.from_bytes(data),
                )
            elif recipe_type.value in (
                "minecraft:smelting",
                "minecraft:blasting",
                "minecraft:smoking",
                "minecraft:campfire_cooking",
            ):
                _data = _DataProxy(
                    group=String.from_bytes(data),
                    category=Varint.from_bytes(data),
                    ingredient=Ingredient.from_bytes(data),
                    result=Slot.from_bytes(data),
                    experience=Float.from_bytes(data),
                    cooking_time=Varint.from_bytes(data),
                )
            elif recipe_type.value == "minecraft:stonecutting":
                _data = _DataProxy(
                    group=String.from_bytes(data),
                    ingredient=Ingredient.from_bytes(data),
                    result=Slot.from_bytes(data),
                )
            elif recipe_type.value == "minecraft:smithing":
                _data = _DataProxy(
                    base=Ingredient.from_bytes(data),
                    addition=Ingredient.from_bytes(data),
                    result=Slot.from_bytes(data),
                )
            elif recipe_type.value == "minecraft:smithing_transform":
                _data = _DataProxy(
                    template=Ingredient.from_bytes(data),
                    base=Ingredient.from_bytes(data),
                    addition=Ingredient.from_bytes(data),
                    result=Slot.from_bytes(data),
                )
            elif recipe_type.value == "minecraft:smithing_trim":
                _data = _DataProxy(
                    template=Ingredient.from_bytes(data),
                    base=Ingredient.from_bytes(data),
                    addition=Ingredient.from_bytes(data),
                )
        return cls(
            recipe_type,
            recipe_id,
            _data,
        )
