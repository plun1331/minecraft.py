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

import json
import struct
from types import FrameType
import uuid
from io import BytesIO
from typing import Any

from nbt import nbt

from .command_parsers import parsers as cmd_parsers
from .enums import (
    CommandParser,
    MapIconType,
    PlayerInfoUpdateActionBits,
    StatCategory,
    StatID,
)

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

__all__ = (
    "BytesIO",  # ext lib, imported for typehints
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
    "Particle",
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
)


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

    def __bool__(self):
        return self.value


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
            raise ValueError(
                f"String length {length.value} exceeds max length {max_length}"
            )
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
                raise ValueError(
                    f"Varint is too big (exceeded max size of {max_size} bytes)"
                )

            if (read & 0b10000000) == 0:
                break

        return cls(result)


class Varlong(Varint):
    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        return super().from_bytes(data, max_size=10)


class EntityMetadataEntry:
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
        return cls(
            Float.from_bytes(data), Float.from_bytes(data), Float.from_bytes(data)
        )


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


class Slot(DataType):
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
        return self.data

    def __len__(self):
        return len(self.data)

    @classmethod
    def from_bytes(cls, data: BytesIO, *, length: int = None) -> Self:
        if length is None:
            return cls(data.read())
        return cls(data.read(length))


class Property(DataType):
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


class Statistic(DataType):
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
        category = StatCategory(Varint.from_bytes(data))
        stat_id = StatID(Varint.from_bytes(data))
        value = Varint.from_bytes(data)
        return cls(category, stat_id, value)


class CommandSuggestionMatch(DataType):
    def __init__(self, match: String, tooltip: Chat | None = None):
        self.match: String = match
        self.tooltip: Chat | None = tooltip

    @property
    def has_tooltip(self):
        return self.tooltip is not None

    def __bytes__(self) -> bytes:
        return (
            bytes(self.match) + bytes(Boolean(self.has_tooltip)) + bytes(self.tooltip)
            if self.has_tooltip
            else b""
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
    def __init__(self, xy: Byte, y: Short, type: Varint, data: NBT):
        self.xz: Byte = xy
        self.y: Short = y
        self.type: Varint = type
        self.data: NBT = data

    @property
    def x(self):
        return self.xz.value >> 4

    @property
    def z(self):
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
        type = MapIconType(Byte.from_bytes(data))
        x = Byte.from_bytes(data)
        y = Byte.from_bytes(data)
        direction = Byte.from_bytes(data)
        has_display_name = Boolean.from_bytes(data)
        display_name = Chat.from_bytes(data) if has_display_name else None
        return cls(type, x, y, direction, display_name)


class Trade(DataType):
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


class _DataProxy(dict):
    def __init__(self, **attrs):
        self.__dict__.update(attrs)

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


class PlayerInfoUpdatePlayer(DataType):
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
    def __init__(
        self,
        parent_id: str | None = None,
        display_data: _DataProxy | None = None,
        criteria: dict[Identifier, None] | None = None,
        requirements: list[list[String]] | None = None,
    ):
        self.parent_id: str | None = parent_id
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
    def __init__(
        self,
        title: Chat,
        description: Chat,
        icon: Identifier,
        frame_type: FrameType,
        flags: Int,
        background_texture: Identifier | None,
        x: float,
        y: float,
    ):
        self.title: Chat = title
        self.description: Chat = description
        self.icon: Slot = icon
        self.frame_type: FrameType = frame_type
        self.flags: int = flags
        self.background_texture: Identifier | None = background_texture
        self.x: float = x
        self.y: float = y

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
