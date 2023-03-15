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

from .datatypes import *
from .enums import BrigadierStringParser


class _Brigadier:
    object_type: Double | Float | Int | Long | Boolean

    def __init__(
        self,
        flags: Byte,
        min_val: Double | Float | Int | Long | Boolean | None = None,
        max_val: Double | Float | Int | Long | Boolean | None = None,
    ):
        self.flags: Byte = flags
        self.min: Double | Float | Int | Long | Boolean = min_val
        self.max: Double | Float | Int | Long | Boolean = max_val

    def __repr__(self):
        return f"{self.__class__.__name__}(min={self.min}, max={self.max})"

    def __bytes__(self):
        _flags = self.flags.value
        return (
            bytes(self.flags)
            + (bytes(self.min) if _flags & 0x01 else b"")
            + (bytes(self.max) if _flags & 0x02 else b"")
        )

    def __len__(self):
        return len(bytes(self))

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        flags = Byte.from_bytes(data)
        _flags = flags.value
        min_val = cls.object_type.from_bytes(data) if _flags & 0x01 else None
        max_val = cls.object_type.from_bytes(data) if _flags & 0x02 else None
        return cls(flags, min_val, max_val)


class BrigadierFloat(_Brigadier):
    # brigadier:float
    object_type = Float


class BrigadierDouble(_Brigadier):
    # brigadier:double
    object_type = Double


class BrigadierInteger(_Brigadier):
    # brigadier:integer
    object_type = Int


class BrigadierLong(_Brigadier):
    # brigadier:long
    object_type = Long


class BrigadierString:
    # brigadier:string
    def __init__(self, value: BrigadierStringParser):
        self.value: BrigadierStringParser = value

    def __repr__(self):
        return f"BrigadierString(value={self.value})"

    def __bytes__(self):
        return bytes(self.value.value.value)

    def __len__(self):
        return len(bytes(self))

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        value = BrigadierStringParser(Varint.from_bytes(data))
        return cls(value)


class _OneFlag:
    def __init__(self, flags: Byte):
        self.flags: Byte = flags

    def __repr__(self):
        return f"{self.__class__.__name__}(flags={self.flags})"

    def __bytes__(self):
        return bytes(self.flags)

    def __len__(self):
        return len(bytes(self))

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        flags = Byte.from_bytes(data)
        _flags = flags.value
        return cls(flags)


class MinecraftEntity(_OneFlag):
    # minecraft:entity
    pass


class MinecraftScoreHolder(_OneFlag):
    # minecraft:score_holder
    pass


class _Identifier:
    def __init__(self, value: Identifier):
        self.registry: Identifier = value

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"

    def __bytes__(self):
        return bytes(self.value)

    def __len__(self):
        return len(bytes(self))

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        value = Identifier.from_bytes(data)
        return cls(value)


class MinecraftResourceOrTag(_Identifier):
    # minecraft:resource_or_tag
    pass


class MinecraftResourceOrTagKey(_Identifier):
    # minecraft:resource_or_tag_key
    pass


class MinecraftResource(_Identifier):
    # minecraft:resource
    pass


class MinecraftResourceKey(_Identifier):
    # minecraft:resource_key
    pass


parsers = {
    1: BrigadierFloat,
    2: BrigadierDouble,
    3: BrigadierInteger,
    4: BrigadierLong,
    5: BrigadierString,
    6: MinecraftEntity,
    29: MinecraftScoreHolder,
    41: MinecraftResourceOrTag,
    42: MinecraftResourceOrTagKey,
    43: MinecraftResource,
    44: MinecraftResourceKey,
}
