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

from typing import Generator

from .base import Packet
from ..datatypes import *
from ..enums import (
    Animation,
    BossBarColor,
    BossBarDivision,
    ChatColor,
    ChatSuggestionAction,
    CollisionRule,
    FeetEyes,
    FilterType,
    GameEvents,
    Hand,
    NameTagVisibility,
    RecipeBookActionType,
    ScoreboardPosition,
    State,
    UpdateObjectiveModes,
    UpdateObjectiveType,
    UpdateScoreAction,
    UpdateTeamModes,
    WorldEvents,
)


class BundleDelimiter(Packet):
    """
    The delimeter for a bundle of packets.
    When received, the client should store every subsequent
    packet it receives, and wait until another delimiter is
    received. Once that happens, the client is guaranteed to
    process every packet in the bundle on the same tick.

    **Packet ID**: ``0x00``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x00
    bound_to = "client"
    state = State.PLAY

    def __init__(self):
        pass

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big")

    @classmethod
    def from_bytes(cls) -> BundleDelimiter:
        return cls()


class SpawnEntity(Packet):
    """
    Sent by the server when a vehicle or other non-living entity is created.

    **Packet ID**: ``0x01``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x01
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        entity_uuid: UUID,
        entity_type: Varint,
        x: Double,
        y: Double,
        z: Double,
        pitch: Angle,
        yaw: Angle,
        head_yaw: Angle,
        data: Varint,
        velocity_x: Short,
        velocity_y: Short,
        velocity_z: Short,
    ):
        self.entity_id = entity_id
        self.entity_uuid = entity_uuid
        self.entity_type = entity_type
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.head_yaw = head_yaw
        self.data: Varint = data
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.velocity_z = velocity_z

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.entity_uuid)
            + bytes(self.entity_type)
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.pitch)
            + bytes(self.yaw)
            + bytes(self.head_yaw)
            + bytes(self.data)
            + bytes(self.velocity_x)
            + bytes(self.velocity_y)
            + bytes(self.velocity_z)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id, entity_uuid, entity_type, x, y, z, pitch,
        # yaw, head_yaw, data, velocity_x, velocity_y, velocity_z
        entity_id = Varint.from_bytes(data)
        # entity_uuid
        entity_uuid = UUID.from_bytes(data)
        # entity_type
        entity_type = Varint.from_bytes(data)
        # x
        x = Double.from_bytes(data)
        # y
        y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # pitch
        pitch = Angle.from_bytes(data)
        # yaw
        yaw = Angle.from_bytes(data)
        # head_yaw
        head_yaw = Angle.from_bytes(data)
        # data
        _data = Varint.from_bytes(data)
        # velocity_x
        velocity_x = Short.from_bytes(data)
        # velocity_y
        velocity_y = Short.from_bytes(data)
        # velocity_z
        velocity_z = Short.from_bytes(data)
        return cls(
            entity_id,
            entity_uuid,
            entity_type,
            x,
            y,
            z,
            pitch,
            yaw,
            head_yaw,
            _data,
            velocity_x,
            velocity_y,
            velocity_z,
        )


class SpawnExperienceOrb(Packet):
    """
    Spawns one or more experience orbs.

    **Packet ID**: ``0x02``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x02
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self, entity_id: Varint, x: Double, y: Double, z: Double, count: Short
    ):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.z = z
        self.count = count

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.count)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), x (double), y (double), z (double), count (short)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # x
        x = Double.from_bytes(data)
        # y
        y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # count
        count = Short.from_bytes(data)
        return cls(entity_id, x, y, z, count)


class SpawnPlayer(Packet):
    """
    This packet is sent by the server when a player comes into visible range, **not** when a player joins.

    **Packet ID**: ``0x03``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x03
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        player_uuid: UUID,
        x: Double,
        y: Double,
        z: Double,
        yaw: Angle,
        pitch: Angle,
    ):
        self.entity_id = entity_id
        self.player_uuid = player_uuid
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.player_uuid)
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.yaw)
            + bytes(self.pitch)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), player_uuid (uuid), x (double), y (double), z (double), yaw (angle), pitch (angle)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # player_uuid
        player_uuid = UUID.from_bytes(data)
        # x
        x = Double.from_bytes(data)
        # y
        y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # yaw
        yaw = Angle.from_bytes(data)
        # pitch
        pitch = Angle.from_bytes(data)
        return cls(entity_id, player_uuid, x, y, z, yaw, pitch)


class EntityAnimation(Packet):
    """
    Sent whenever an entity should change animation.

    **Packet ID**: ``0x04``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x04
    bound_to = "client"
    state = State.PLAY

    def __init__(self, entity_id: Varint, animation: Animation):
        self.entity_id = entity_id
        self.animation = animation

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.animation)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), animation_id (varint)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # animation
        animation = Animation.from_value(UnsignedByte.from_bytes(data))
        return cls(entity_id, animation)


class AwardStats(Packet):
    """
    Sent as a response to Client Command (id 1).
    Will only send the changed values if previously requested.

    **Packet ID**: ``0x05``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x05
    bound_to = "client"
    state = State.PLAY

    def __init__(self, stats: list[tuple[Varint, Varint]]):
        self.stats = stats

    def __bytes__(self):
        ...

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: player_uuid (uuid), stats (list of tuples of varints)
        # count
        count = Varint.from_bytes(data)
        # stats
        stats = []
        for _ in range(count.value):
            stats.append(Statistic.from_bytes(data))


class AcknowledgeBlockChange(Packet):
    """
    Acknowledges a user-initiated block change.
    After receiving this packet, the client should display the block state
    sent by the server instead of the one predicted by the client.

    **Packet ID**: ``0x06``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x06
    bound_to = "client"
    state = State.PLAY

    def __init__(self, sequence_id: Varint):
        self.sequence_id: Varint = sequence_id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.sequence_id)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: sequence_id (varint)
        # sequence_id
        sequence_id = Varint.from_bytes(data)
        return cls(sequence_id)


class SetBlockDestroyStage(Packet):
    """
    0-9 are the displayable destroy stages and each other
    number means that there is no animation on this coordinate.

    **Packet ID**: ``0x07``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x07
    bound_to = "client"
    state = State.PLAY

    def __init__(self, entity_id: Varint, location: Position, destroy_stage: Byte):
        self.entity_id: Varint = entity_id
        self.location: Position = location
        self.destroy_stage: Byte = destroy_stage

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.location)
            + bytes(self.destroy_stage)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), location (position), destroy_stage (byte)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # location
        location = Position.from_bytes(data)
        # destroy_stage
        destroy_stage = Byte.from_bytes(data)
        return cls(entity_id, location, destroy_stage)


class BlockEntityData(Packet):
    """
    Sets the block entity associated with the block at the given location.

    **Packet ID**: ``0x08``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x08
    bound_to = "client"
    state = State.PLAY

    def __init__(self, location: Position, type: Varint, nbt_data: NBT):
        self.location: Position = location
        self.type: Varint = type
        self.nbt_data: NBT = nbt_data

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.location)
            + bytes(self.type)
            + bytes(self.nbt_data)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: location (position), type (varint), nbt_data (nbt)
        # location
        location = Position.from_bytes(data)
        # type
        type = Varint.from_bytes(data)
        # nbt_data
        nbt_data = NBT.from_bytes(data)
        return cls(location, type, nbt_data)


class BlockAction(Packet):
    """
    This packet is used for a number of actions and animations performed by blocks,
    usually non-persistent.
    The client should ignore the provided block type and instead uses the block state
    in their world.

    **Packet ID**: ``0x09``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x09
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        location: Position,
        action_id: UnsignedByte,
        action_param: UnsignedByte,
        block_type: Varint,
    ):
        self.location: Position = location
        self.action_id: UnsignedByte = action_id
        self.action_param: UnsignedByte = action_param
        self.block_type: Varint = block_type

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.location)
            + bytes(self.action_id)
            + bytes(self.action_param)
            + bytes(self.block_type)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: location (position), action_id (unsigned byte), action_param (unsigned byte), block_type (varint)
        # location
        location = Position.from_bytes(data)
        # action_id
        action_id = UnsignedByte.from_bytes(data)
        # action_param
        action_param = UnsignedByte.from_bytes(data)
        # block_type
        block_type = Varint.from_bytes(data)
        return cls(location, action_id, action_param, block_type)


class BlockUpdate(Packet):
    """
    Fired whenever a block is changed within the render distance.

    **Packet ID**: ``0x0A``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x0A
    bound_to = "client"
    state = State.PLAY

    def __init__(self, location: Position, block_id: Varint):
        self.location: Position = location
        self.block_id: Varint = block_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.location)
            + bytes(self.block_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: location (position), block_id (varint)
        # location
        location = Position.from_bytes(data)
        # block_id
        block_id = Varint.from_bytes(data)
        return cls(location, block_id)


class BossBar(Packet):
    """
    Sent by the server to update the boss bar on the client.

    **Packet ID**: ``0x0B``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x0B
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        uuid: UUID,
        action: UnsignedByte,
        title: Chat | None,
        health: Float | None,
        color: BossBarColor | None,
        division: BossBarDivision | None,
        flags: UnsignedByte | None,
    ):
        self.uuid: UUID = uuid
        self.action: UnsignedByte = action
        self.title: Chat | None = title
        self.health: Float | None = health
        self.color: BossBarColor | None = color
        self.division: BossBarDivision | None = division
        self.flags: UnsignedByte | None = flags

    def __bytes__(self):
        res = self.packet_id.to_bytes(1, "big") + bytes(self.uuid) + bytes(self.action)
        match self.action.value:
            case 0:
                res += (
                    bytes(self.title)
                    + bytes(self.health)
                    + bytes(self.color.value)  # type: ignore
                    + bytes(self.division.value)  # type: ignore
                    + bytes(self.flags)  # type: ignore
                )
            case 1:
                pass
            case 2:
                res += bytes(self.health)
            case 3:
                res += bytes(self.title)
            case 4:
                res += bytes(self.color.value) + bytes(  # type: ignore
                    self.division.value  # type: ignore
                )
            case 5:
                res += bytes(self.flags)
            case _:
                raise ValueError(f"Invalid action value {self.action.value}")
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: uuid (uuid), action (unsigned byte),
        # title (chat), health (float), color (varint),
        # division (varint), flags (unsigned byte)
        # uuid
        uuid = UUID.from_bytes(data)
        # action
        action = UnsignedByte.from_bytes(data)
        # title, health, color, division, flags
        title = health = color = division = flags = None
        match action.value:
            case 0:
                title = Chat.from_bytes(data)
                health = Float.from_bytes(data)
                color = BossBarColor.from_value(Varint.from_bytes(data))
                division = Varint.from_bytes(data)
                flags = UnsignedByte.from_bytes(data)
            case 1:
                pass
            case 2:
                health = Float.from_bytes(data)
            case 3:
                title = Chat.from_bytes(data)
            case 4:
                color = BossBarColor.from_value(Varint.from_bytes(data))
                division = Varint.from_bytes(data)
            case 5:
                flags = UnsignedByte.from_bytes(data)
            case _:
                raise ValueError(f"Invalid action value {action.value}")
        return cls(uuid, action, title, health, color, division, flags)


class ChangeDifficulty(Packet):
    """
    Changes the difficulty setting in the client's option menu.

    **Packet ID**: ``0x0C``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x0C
    bound_to = "client"
    state = State.PLAY

    def __init__(self, difficulty: UnsignedByte, locked: Boolean = Boolean(False)):
        self.difficulty: UnsignedByte = difficulty
        self.locked: Boolean = locked

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.difficulty)
            + bytes(self.locked)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: difficulty (unsigned byte), locked (boolean)
        # difficulty
        difficulty = UnsignedByte.from_bytes(data)

        locked = Boolean.from_bytes(data)
        return cls(difficulty, locked)


class ChunkBiomes(Packet):
    """
    Sent by the server to update the biomes within a chunk.

    **Packet ID**: ``0x0D``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x0D
    bound_to = "client"
    state = State.PLAY

    def __init__(self, chunk_biome_data: list[_DataProxy]):
        self.chunk_biome_data: list[_DataProxy] = chunk_biome_data

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(Varint(len(self.chunk_biome_data)))
            + b"".join(
                (
                    bytes(biome.chunk_x)
                    + bytes(biome.chunk_z)
                    + bytes(len(biome.data))
                    + bytes(biome.data)
                )
                for biome in self.chunk_biome_data
            )
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: chunk_biome_data (list of chunk biome data)
        # chunk_biome_data
        chunk_biome_data = []
        for _ in range(Varint.from_bytes(data).value):
            chunk_biome_data.append(
                _DataProxy(
                    chunk_x=Int.from_bytes(data),
                    chunk_z=Int.from_bytes(data),
                    data=ByteArray.from_bytes(
                        data, length=Varint.from_bytes(data).value
                    ),
                ),
            )
        return cls(chunk_biome_data)


class ClearTitles(Packet):
    """
    Clear the client's current title information, with the option to also reset it.

    **Packet ID**: ``0x0E``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x0E
    bound_to = "client"
    state = State.PLAY

    def __init__(self, reset: Boolean):
        self.reset: Boolean = reset

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.reset)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: reset (boolean)
        # reset
        reset = Boolean.from_bytes(data)
        return cls(reset)


class CommandSuggestionsResponse(Packet):
    """
    The server responds with a list of auto-completions of the last word sent to it.

    **Packet ID**: ``0x0F``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x0F
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        transaction_id: Varint,
        start: Varint,
        length: Varint,
        matches: list[CommandSuggestionMatch],
    ):
        self.transaction_id: Varint = transaction_id
        self.start: Varint = start
        self.length: Varint = length
        self.matches: list[CommandSuggestionMatch] = matches

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.transaction_id)
            + bytes(Varint(len(self.matches)))
            + b"".join(bytes(match) for match in self.matches)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: transaction_id (varint), start (varint), length (varint), suggestions (list of chat)
        # transaction_id
        transaction_id = Varint.from_bytes(data)
        # start
        start = Varint.from_bytes(data)
        # length
        length = Varint.from_bytes(data)
        # suggestions
        count = Varint.from_bytes(data).value
        matches = []
        for _ in range(count):
            matches.append(CommandSuggestionMatch.from_bytes(data))
        return cls(transaction_id, start, length, matches)


class Commands(Packet):
    """
    lists all of the commands on the server, and how they are parsed.

    **Packet ID**: ``0x10``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x10
    bound_to = "client"
    state = State.PLAY

    def __init__(self, nodes: list[CommandNode], root_index: Varint):
        self.nodes: list[CommandNode] = nodes
        self.root_index: Varint = root_index

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(Varint(len(self.nodes)))
            + b"".join(bytes(node) for node in self.nodes)
            + bytes(self.root_index)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: nodes (list of command nodes), root_index (varint)
        # nodes
        count = Varint.from_bytes(data).value
        nodes = []
        for _ in range(count):
            nodes.append(CommandNode.from_bytes(data))
        # root_index
        root_index = Varint.from_bytes(data)
        return cls(nodes, root_index)


class CloseContainer(Packet):
    """
    This packet is sent from the server to the client when a window is forcibly closed,
    such as when a chest is destroyed while it's open.

    **Packet ID**: ``0x11``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x11
    bound_to = "client"
    state = State.PLAY

    def __init__(self, window_id: UnsignedByte):
        self.window_id: UnsignedByte = window_id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.window_id)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (unsigned byte)
        # window_id
        window_id = UnsignedByte.from_bytes(data)
        return cls(window_id)


class SetContainerContents(Packet):
    """
    Sent by the server when items in multiple slots (in a window) are added/removed.
    This includes the main inventory, equipped armour and crafting slots.
    This packet with Window ID set to "0" is sent during the player joining sequence
    to initialise the player's inventory.

    **Packet ID**: ``0x12``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x12
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        window_id: UnsignedByte,
        state_id: Varint,
        contents: list[Slot],
        carried_item: Slot,
    ):
        self.window_id: UnsignedByte = window_id
        self.state_id: Varint = state_id
        self.contents: list[Slot] = contents
        self.carried_item: Slot = carried_item

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(self.state_id)
            + bytes(Varint(len(self.contents)))
            + b"".join(bytes(slot) for slot in self.contents)
            + bytes(self.carried_item)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (unsigned byte), state_id (varint), contents (list of slots), carried_item (slot)
        # window_id
        window_id = UnsignedByte.from_bytes(data)
        # state_id
        state_id = Varint.from_bytes(data)
        # contents
        count = Varint.from_bytes(data).value
        contents = []
        for _ in range(count):
            contents.append(Slot.from_bytes(data))
        # carried_item
        carried_item = Slot.from_bytes(data)
        return cls(window_id, state_id, contents, carried_item)


class SetContainerProperty(Packet):
    """
    This packet is used to inform the client that part of a GUI window should be updated.

    **Packet ID**: ``0x13``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x13
    bound_to = "client"
    state = State.PLAY

    def __init__(self, window_id: UnsignedByte, property: Short, value: Short):
        self.window_id: UnsignedByte = window_id
        self.property: Short = property
        self.value: Short = value

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(self.property)
            + bytes(self.value)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (unsigned byte), property (short), value (short)
        # window_id
        window_id = UnsignedByte.from_bytes(data)
        # property
        property = Short.from_bytes(data)
        # value
        value = Short.from_bytes(data)
        return cls(window_id, property, value)


class SetContainerSlot(Packet):
    """
    Sent by the server when an item in a slot (in a window) is added/removed.

    **Packet ID**: ``0x14``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x14
    bound_to = "client"
    state = State.PLAY

    def __init__(self, window_id: Byte, state_id: Varint, slot: Short, item: Slot):
        self.window_id: Byte = window_id
        self.state_id: Varint = state_id
        self.slot: Short = slot
        self.item: Slot = item

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(self.state_id)
            + bytes(self.slot)
            + bytes(self.item)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (byte), state_id (varint), slot (short), item (slot)
        # window_id
        window_id = Byte.from_bytes(data)
        # state_id
        state_id = Varint.from_bytes(data)
        # slot
        slot = Short.from_bytes(data)
        # item
        item = Slot.from_bytes(data)
        return cls(window_id, state_id, slot, item)


class SetCooldown(Packet):
    """
    This packet is used to inform the client that a cooldown should be started for an item.

    **Packet ID**: ``0x15``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x15
    bound_to = "client"
    state = State.PLAY

    def __init__(self, item_id: Varint, cooldown: Varint):
        self.item_id: Varint = item_id
        self.cooldown: Varint = cooldown

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.item_id)
            + bytes(self.cooldown)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: item_id (varint), cooldown (varint)
        # item_id
        item_id = Varint.from_bytes(data)
        # cooldown
        cooldown = Varint.from_bytes(data)
        return cls(item_id, cooldown)


class ChatSuggestions(Packet):
    """
    Unused by the default server.
    Likely provided for custom servers to send chat message completions to clients.

    **Packet ID**: ``0x16``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x16
    bound_to = "client"
    state = State.PLAY

    def __init__(self, action: ChatSuggestionAction, entries: list[String]):
        self.action: ChatSuggestionAction = action
        self.entries: list[String] = entries

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.action.value)
            + bytes(Varint(len(self.entries)))  # type: ignore
            + b"".join(bytes(entry) for entry in self.entries)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: action (varint), entries (varint, string[])
        # action
        action = ChatSuggestionAction(Varint.from_bytes(data).value)
        # entries
        count = Varint.from_bytes(data).value
        entries = []
        for _ in range(count):
            entries.append(String.from_bytes(data))
        return cls(action, entries)


class PluginMessageClientbound(Packet):
    """
    Mods and plugins can use this to send their data.
    Minecraft itself uses several plugin channels.
    These internal channels are in the minecraft namespace.

    **Packet ID**: ``0x17``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x17
    bound_to = "client"
    state = State.PLAY

    def __init__(self, channel: Identifier, data: ByteArray):
        self.channel: Identifier = channel
        self.data: ByteArray = data

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") + bytes(self.channel) + bytes(self.data)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: channel (identifier), data (byte array)
        # channel
        channel = Identifier.from_bytes(data)
        # data
        data = ByteArray.from_bytes(data)
        return cls(channel, data)


class DamageEvent(Packet):
    """
    Sent by the server to make the player take damage.

    **Packet ID**: ``0x18``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x18
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        source_type_id: Varint,
        source_cause_id: Varint,
        source_direct_id: Varint,
        source_position_x: Double | None = None,
        source_position_y: Double | None = None,
        source_position_z: Double | None = None,
    ):
        self.entity_id: Varint = entity_id
        self.source_type_id: Varint = source_type_id
        self.source_cause_id: Varint = source_cause_id
        self.source_direct_id: Varint = source_direct_id
        self.source_position_x: Double | None = source_position_x
        self.source_position_y: Double | None = source_position_y
        self.source_position_z: Double | None = source_position_z

    def __bytes__(self):
        ret = (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.source_type_id)
            + bytes(self.source_cause_id)
            + bytes(self.source_direct_id)
            + bytes(Boolean(self.source_position_x is not None))
        )
        if self.source_position_x is not None:
            ret += (
                bytes(self.source_position_x)
                + bytes(self.source_position_y)
                + bytes(self.source_position_z)
            )
        return ret

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), source_type_id (varint),
        # source_cause_id (varint), source_direct_id (varint),
        # source_position_x (double), source_position_y (double),
        # source_position_z (double)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # source_type_id
        source_type_id = Varint.from_bytes(data)
        # source_cause_id
        source_cause_id = Varint.from_bytes(data)
        # source_direct_id
        source_direct_id = Varint.from_bytes(data)
        # source position
        source_position_x = None
        source_position_y = None
        source_position_z = None
        if Boolean.from_bytes(data).value:
            # source_position_x
            source_position_x = Double.from_bytes(data)
            # source_position_y
            source_position_y = Double.from_bytes(data)
            # source_position_z
            source_position_z = Double.from_bytes(data)
        return cls(
            entity_id,
            source_type_id,
            source_cause_id,
            source_direct_id,
            source_position_x,
            source_position_y,
            source_position_z,
        )


class DeleteMessage(Packet):
    """
    Sent by the server to delete a message from the client's chat.

    **Packet ID**: ``0x19``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x19
    bound_to = "client"
    state = State.PLAY

    def __init__(self, signature: ByteArray):
        self.signature: ByteArray = signature

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + len(self.signature).to_bytes(1, "big")
            + bytes(self.signature)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: signature (byte array)
        # signature
        length = Varint.from_bytes(data).value
        signature = ByteArray.from_bytes(data, length=length)
        return cls(signature)


class DisconnectPlay(Packet):
    """
    Sent by the server before it disconnects a client.
    The client should assume that the server has already
    closed the connection by the time the packet arrives.

    **Packet ID**: ``0x1A``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x1A
    bound_to = "client"
    state = State.PLAY

    def __init__(self, reason: Chat):
        self.reason: Chat = reason

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.reason)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: reason (chat)
        # reason
        reason = Chat.from_bytes(data)
        return cls(reason)


class DisguisedChatMessage(Packet):
    """
    Used to send system chat messages to the client.

    **Packet ID**: ``0x1B``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x1B
    bound_to = "client"
    state = State.PLAY

    def __init__(self, message: String):
        self.message: String = message

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.message)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: message (string)
        # message
        message = String.from_bytes(data)
        return cls(message)


class EntityEvent(Packet):
    """
    Entity statuses generally trigger an animation for an entity.

    **Packet ID**: ``0x1C``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x1C
    bound_to = "client"
    state = State.PLAY

    def __init__(self, entity_id: Varint, entity_status: Byte):
        self.entity_id: Varint = entity_id
        self.entity_status: Byte = entity_status

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.entity_status.value)  # type: ignore
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), entity_status (byte)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # entity_status
        entity_status = Byte.from_bytes(data)
        return cls(entity_id, entity_status)


class Explosion(Packet):
    """
    Sent when an explosion occurs (creepers, TNT, and ghast fireballs).

    **Packet ID**: ``0x1D``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x1D
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        x: Double,
        y: Double,
        z: Double,
        strength: Float,
        records: list[tuple[Byte, Byte, Byte]],
        player_motion_x: Float,
        player_motion_y: Float,
        player_motion_z: Float,
    ):
        self.x: Double = x
        self.y: Double = y
        self.z: Double = z
        self.strength: Float = strength
        self.records: list[tuple[Byte, Byte, Byte]] = records
        self.player_motion_x: Float = player_motion_x
        self.player_motion_y: Float = player_motion_y
        self.player_motion_z: Float = player_motion_z

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.strength)
            + len(self.records).to_bytes(1, "big")
            + b"".join(
                b"".join(bytes(block) for block in record) for record in self.records
            )
            + bytes(self.player_motion_x)
            + bytes(self.player_motion_y)
            + bytes(self.player_motion_z)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: x (double), y (double), z (double), strength (float),
        # records (array of records), player_motion_x (float),
        # player_motion_y (float), player_motion_z (float)
        # x
        x = Double.from_bytes(data)
        # y
        y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # strength
        strength = Float.from_bytes(data)
        # records
        count = Varint.from_bytes(data).value
        records = []
        for _ in range(count):
            records.append(
                (Byte.from_bytes(data), Byte.from_bytes(data), Byte.from_bytes(data))
            )
        # player_motion_x
        player_motion_x = Float.from_bytes(data)
        # player_motion_y
        player_motion_y = Float.from_bytes(data)
        # player_motion_z
        player_motion_z = Float.from_bytes(data)
        return cls(
            x,
            y,
            z,
            strength,
            records,
            player_motion_x,
            player_motion_y,
            player_motion_z,
        )


class UnloadChunk(Packet):
    """
    Tells the client to unload a chunk.

    **Packet ID**: ``0x1E``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x1E
    bound_to = "client"
    state = State.PLAY

    def __init__(self, x: Int, z: Int):
        self.x: Int = x
        self.z: Int = z

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.x) + bytes(self.z)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: x (int), z (int)
        # x
        x = Int.from_bytes(data)
        # z
        z = Int.from_bytes(data)
        return cls(x, z)


class GameEvent(Packet):
    """
    Used for a wide variety of game events, from weather to bed use to gamemode to demo messages.

    **Packet ID**: ``0x1F``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x1F
    bound_to = "client"
    state = State.PLAY

    def __init__(self, event: GameEvents, value: Float):
        self.event: GameEvents = event
        self.value: Float = value

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.event.value)
            + bytes(self.value)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: event_id (varint), value (float)
        # event_id
        event = GameEvents.from_value(UnsignedByte.from_bytes(data))
        # value
        value = Float.from_bytes(data)
        return cls(event, value)


class OpenHorseScreen(Packet):
    """
    Opens the horse inventory screen.

    **Packet ID**: ``0x20``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x20
    bound_to = "client"
    state = State.PLAY

    def __init__(self, window_id: UnsignedByte, slot_count: Varint, entity_id: Int):
        self.window_id: UnsignedByte = window_id
        self.slot_count: Varint = slot_count
        self.entity_id: Int = entity_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(self.slot_count)
            + bytes(self.entity_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (unsigned byte), slot_count (varint), entity_id (int)
        # window_id
        window_id = UnsignedByte.from_bytes(data)
        # slot_count
        slot_count = Varint.from_bytes(data)
        # entity_id
        entity_id = Int.from_bytes(data)
        return cls(window_id, slot_count, entity_id)


class HurtAnimation(Packet):
    """
    Plays a bobbing animation for the entity receiving damage.

    **Packet ID**: ``0x21``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x21
    bound_to = "client"
    state = State.PLAY

    def __init__(self, entity_id: Varint, yaw: Float):
        self.entity_id: Varint = entity_id
        self.yaw: Float = yaw

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") + bytes(self.entity_id) + bytes(self.yaw)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), yaw (float)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # yaw
        yaw = Float.from_bytes(data)
        return cls(entity_id, yaw)


class InitializeWorldBorder(Packet):
    """
    Initializes the world border.

    **Packet ID**: ``0x22``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x22
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        x: Double,
        z: Double,
        old_diameter: Double,
        new_diameter: Double,
        speed: Varlong,
        portal_teleport_boundary: Varint,
        warning_time: Varint,
        warning_blocks: Varint,
    ):
        self.x: Double = x
        self.z: Double = z
        self.old_diameter: Double = old_diameter
        self.new_diameter: Double = new_diameter
        self.speed: Varlong = speed
        self.portal_teleport_boundary: Varint = portal_teleport_boundary
        self.warning_time: Varint = warning_time
        self.warning_blocks: Varint = warning_blocks

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.x)
            + bytes(self.z)
            + bytes(self.old_diameter)
            + bytes(self.new_diameter)
            + bytes(self.speed)
            + bytes(self.portal_teleport_boundary)
            + bytes(self.warning_time)
            + bytes(self.warning_blocks)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: x (double), z (double), old_diameter (double), new_diameter (double),
        # speed (varlong), portal_teleport_boundary (varint), warning_time (varint),
        # warning_blocks (varint)
        # x
        x = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # old_diameter
        old_diameter = Double.from_bytes(data)
        # new_diameter
        new_diameter = Double.from_bytes(data)
        # speed
        speed = Varlong.from_bytes(data)
        # portal_teleport_boundary
        portal_teleport_boundary = Varint.from_bytes(data)
        # warning_time
        warning_time = Varint.from_bytes(data)
        # warning_blocks
        warning_blocks = Varint.from_bytes(data)
        return cls(
            x,
            z,
            old_diameter,
            new_diameter,
            speed,
            portal_teleport_boundary,
            warning_time,
            warning_blocks,
        )


class KeepAliveClientbound(Packet):
    """
    The server will frequently send out a keep-alive, each containing a random ID.
    The client must respond with the same payload (see serverbound Keep Alive).
    If the client does not respond to them for over 30 seconds,
    the server kicks the client.
    Vice versa, if the server does not send any keep-alives for 20 seconds,
    the client will disconnect and yields a "Timed out" exception.

    **Packet ID**: ``0x23``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x23
    bound_to = "client"
    state = State.PLAY

    def __init__(self, keep_alive_id: Long):
        self.keep_alive_id: Long = keep_alive_id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.keep_alive_id)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: keep_alive_id (long)
        # keep_alive_id
        keep_alive_id = Long.from_bytes(data)
        return cls(keep_alive_id)


class ChunkDataAndUpdateLight(Packet):
    """
    A chunk data packet with the light data included.

    **Packet ID**: ``0x24``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x24
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        chunk_x: Int,
        chunk_z: Int,
        heightmaps: NBT,
        data: ByteArray,
        block_entities: list[BlockEntity],
        trust_edges: Boolean,
        sky_light_mask: BitSet,
        block_light_mask: BitSet,
        empty_sky_light_mask: BitSet,
        empty_block_light_mask: BitSet,
        sky_light: list[ByteArray],
        block_light: list[ByteArray],
    ):
        self.chunk_x: Int = chunk_x
        self.chunk_z: Int = chunk_z
        self.heightmaps: NBT = heightmaps
        self.data: ByteArray = data
        self.block_entities: list[BlockEntity] = block_entities
        self.trust_edges: Boolean = trust_edges
        self.sky_light_mask: BitSet = sky_light_mask
        self.block_light_mask: BitSet = block_light_mask
        self.empty_sky_light_mask: BitSet = empty_sky_light_mask
        self.empty_block_light_mask: BitSet = empty_block_light_mask
        self.sky_light: list[ByteArray] = sky_light
        self.block_light: list[ByteArray] = block_light

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.chunk_x)
            + bytes(self.chunk_z)
            + bytes(self.heightmaps)
            + bytes(self.data)
            + bytes(Varint(len(self.block_entities)))
            + b"".join([bytes(i) for i in self.block_entities])
            + bytes(self.trust_edges)
            + bytes(self.sky_light_mask)
            + bytes(self.block_light_mask)
            + bytes(self.empty_sky_light_mask)
            + bytes(self.empty_block_light_mask)
            + bytes(Varint(len(self.sky_light)))
            + b"".join([bytes(Varint(len(i))) + bytes(i) for i in self.sky_light])
            + bytes(Varint(len(self.block_light)))
            + b"".join([bytes(Varint(len(i))) + bytes(i) for i in self.block_light])
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: chunk_x (int), chunk_z (int), heightmaps (nbt), data (byte array),
        # block_entities (list[block entity]), trust_edges (boolean),
        # sky_light_mask (bit set), block_light_mask (bit set),
        # empty_sky_light_mask (bit set), empty_block_light_mask (bit set),
        # sky_light (list[list[bytes]]), block_light (list[list[bytes]])
        # chunk_x
        chunk_x = Int.from_bytes(data)
        # chunk_z
        chunk_z = Int.from_bytes(data)
        # heightmaps
        heightmaps = NBT.from_bytes(data)
        # data
        data_size = Varint.from_bytes(data).value
        _data = ByteArray.from_bytes(data, length=data_size)
        # block_entities
        block_entities_size = Varint.from_bytes(data).value
        block_entities = []
        for _ in range(block_entities_size):
            block_entities.append(BlockEntity.from_bytes(data))
        # trust_edges
        trust_edges = Boolean.from_bytes(data)
        # sky_light_mask
        sky_light_mask = BitSet.from_bytes(data)
        # block_light_mask
        block_light_mask = BitSet.from_bytes(data)
        # empty_sky_light_mask
        empty_sky_light_mask = BitSet.from_bytes(data)
        # empty_block_light_mask
        empty_block_light_mask = BitSet.from_bytes(data)
        # sky_light
        sky_light_size = Varint.from_bytes(data).value
        sky_light = []
        for _ in range(sky_light_size):
            arr_length = Varint.from_bytes(data).value
            sky_light.append(ByteArray.from_bytes(data, length=arr_length))
        # block_light
        block_light_size = Varint.from_bytes(data).value
        block_light = []
        for _ in range(block_light_size):
            arr_length = Varint.from_bytes(data).value
            block_light.append(ByteArray.from_bytes(data, length=arr_length))
        return cls(
            chunk_x,
            chunk_z,
            heightmaps,
            _data,
            block_entities,
            trust_edges,
            sky_light_mask,
            block_light_mask,
            empty_sky_light_mask,
            empty_block_light_mask,
            sky_light,
            block_light,
        )


class WorldEvent(Packet):
    """
    Sent when a client is to play a sound or particle effect.

    **Packet ID**: ``0x25``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x25
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        event: WorldEvents,
        location: Position,
        data: Int,
        disable_relative_volume: Boolean,
    ):
        self.event: WorldEvents = event
        self.location: Position = location
        self.data: Int = data
        self.disable_relative_volume: Boolean = disable_relative_volume

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.event.value)
            + bytes(self.location)
            + bytes(self.data)
            + bytes(self.disable_relative_volume)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: event_id (int), location (position), data (int),
        # disable_relative_volume (boolean)
        # event_id
        event = WorldEvents.from_value(Int.from_bytes(data))
        # location
        location = Position.from_bytes(data)
        # data
        _data = Int.from_bytes(data)
        # disable_relative_volume
        disable_relative_volume = Boolean.from_bytes(data)
        return cls(event, location, _data, disable_relative_volume)


class Particle(Packet):
    """
    Displays the named particle.

    **Packet ID**: ``0x26``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x26
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        particle_id: Varint,
        long_distance: Boolean,
        x: Double,
        y: Double,
        z: Double,
        offset_x: Float,
        offset_y: Float,
        offset_z: Float,
        max_speed: Float,
        particle_count: Int,
        particle_data: bytes,
    ):
        self.particle_id: Varint = particle_id
        self.long_distance: Boolean = long_distance
        self.x: Double = x
        self.y: Double = y
        self.z: Double = z
        self.offset_x: Float = offset_x
        self.offset_y: Float = offset_y
        self.offset_z: Float = offset_z
        self.max_speed: Float = max_speed
        self.particle_count: Int = particle_count
        self.particle_data: bytes = particle_data

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.particle_id)
            + bytes(self.long_distance)
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.offset_x)
            + bytes(self.offset_y)
            + bytes(self.offset_z)
            + bytes(self.max_speed)
            + bytes(self.particle_count)
            + bytes(self.particle_data)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: particle_id (varint), long_distance (boolean), x (double),
        # y (double), z (double), offset_x (float), offset_y (float),
        # offset_z (float), max_speed (float), particle_count (int),
        # particle_data (bytes)
        # particle_id
        particle_id = Varint.from_bytes(data)
        # long_distance
        long_distance = Boolean.from_bytes(data)
        # x
        x = Double.from_bytes(data)
        # y
        y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # offset_x
        offset_x = Float.from_bytes(data)
        # offset_y
        offset_y = Float.from_bytes(data)
        # offset_z
        offset_z = Float.from_bytes(data)
        # max_speed
        max_speed = Float.from_bytes(data)
        # particle_count
        particle_count = Int.from_bytes(data)
        # particle_data
        particle_data = data.read()
        return cls(
            particle_id,
            long_distance,
            x,
            y,
            z,
            offset_x,
            offset_y,
            offset_z,
            max_speed,
            particle_count,
            particle_data,
        )


class UpdateLight(Packet):
    """
    Updates light levels for a chunk.

    **Packet ID**: ``0x27``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x27
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        chunk_x: Int,
        chunk_z: Int,
        trust_edges: Boolean,
        sky_light_mask: BitSet,
        block_light_mask: BitSet,
        empty_sky_light_mask: BitSet,
        empty_block_light_mask: BitSet,
        sky_light: list[ByteArray],
        block_light: list[ByteArray],
    ):
        self.chunk_x: Int = chunk_x
        self.chunk_z: Int = chunk_z
        self.trust_edges: Boolean = trust_edges
        self.sky_light_mask: BitSet = sky_light_mask
        self.block_light_mask: BitSet = block_light_mask
        self.empty_sky_light_mask: BitSet = empty_sky_light_mask
        self.empty_block_light_mask: BitSet = empty_block_light_mask
        self.sky_light: list[ByteArray] = sky_light
        self.block_light: list[ByteArray] = block_light

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.chunk_x)
            + bytes(self.chunk_z)
            + bytes(self.trust_edges)
            + bytes(self.sky_light_mask)
            + bytes(self.block_light_mask)
            + bytes(self.empty_sky_light_mask)
            + bytes(self.empty_block_light_mask)
            + bytes(Varint(len(self.sky_light)))
            + b"".join([bytes(Varint(len(i))) + bytes(i) for i in self.sky_light])
            + bytes(Varint(len(self.block_light)))
            + b"".join([bytes(Varint(len(i))) + bytes(i) for i in self.block_light])
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: chunk_x (int), chunk_z (int), trust_edges (boolean),
        # sky_light_mask (bit set), block_light_mask (bit set),
        # empty_sky_light_mask (bit set), empty_block_light_mask (bit set),
        # sky_light (list[list[bytes]]), block_light (list[list[bytes]])
        # chunk_x
        chunk_x = Int.from_bytes(data)
        # chunk_z
        chunk_z = Int.from_bytes(data)
        # trust_edges
        trust_edges = Boolean.from_bytes(data)
        # sky_light_mask
        sky_light_mask = BitSet.from_bytes(data)
        # block_light_mask
        block_light_mask = BitSet.from_bytes(data)
        # empty_sky_light_mask
        empty_sky_light_mask = BitSet.from_bytes(data)
        # empty_block_light_mask
        empty_block_light_mask = BitSet.from_bytes(data)
        # sky_light
        sky_light_size = Varint.from_bytes(data).value
        sky_light = []
        for _ in range(sky_light_size):
            arr_length = Varint.from_bytes(data).value
            sky_light.append(ByteArray.from_bytes(data, length=arr_length))
        # block_light
        block_light_size = Varint.from_bytes(data).value
        block_light = []
        for _ in range(block_light_size):
            arr_length = Varint.from_bytes(data).value
            block_light.append(ByteArray.from_bytes(data, length=arr_length))
        return cls(
            chunk_x,
            chunk_z,
            trust_edges,
            sky_light_mask,
            block_light_mask,
            empty_sky_light_mask,
            empty_block_light_mask,
            sky_light,
            block_light,
        )


class LoginPlay(Packet):
    """
    Updates some data about the player.

    **Packet ID**: ``0x28``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x28
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Int,
        is_hardcore: Boolean,
        gamemode: UnsignedByte,
        previous_gamemode: Byte,
        dimensions: list[Identifier],
        registry_codec: NBT,
        dimension_type: Identifier,
        dimension_name: Identifier,
        hashed_seed: Long,
        max_players: Varint,
        view_distance: Varint,
        simulation_distance: Varint,
        reduced_debug_info: Boolean,
        enable_respawn_screen: Boolean,
        is_debug: Boolean,
        is_flat: Boolean,
        death_dimension_name: Identifier | None = None,
        death_location: Position | None = None,
    ):
        self.entity_id: Int = entity_id
        self.is_hardcore: Boolean = is_hardcore
        self.gamemode: UnsignedByte = gamemode
        self.previous_gamemode: Byte = previous_gamemode
        self.dimensions: list[Identifier] = dimensions
        self.registry_codec: NBT = registry_codec
        self.dimension_type: Identifier = dimension_type
        self.dimension_name: Identifier = dimension_name
        self.hashed_seed: Long = hashed_seed
        self.max_players: Varint = max_players
        self.view_distance: Varint = view_distance
        self.simulation_distance: Varint = simulation_distance
        self.reduced_debug_info: Boolean = reduced_debug_info
        self.enable_respawn_screen: Boolean = enable_respawn_screen
        self.is_debug: Boolean = is_debug
        self.is_flat: Boolean = is_flat
        self.death_dimension_name: Identifier | None = death_dimension_name
        self.death_location: Position | None = death_location

    @property
    def has_death_location(self) -> bool:
        return self.death_location is not None

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.is_hardcore)
            + bytes(self.gamemode)
            + bytes(self.previous_gamemode)
            + bytes(Varint(len(self.dimensions)))
            + b"".join([bytes(i) for i in self.dimensions])
            + bytes(self.registry_codec)
            + bytes(self.dimension_type)
            + bytes(self.dimension_name)
            + bytes(self.hashed_seed)
            + bytes(self.max_players)
            + bytes(self.view_distance)
            + bytes(self.simulation_distance)
            + bytes(self.reduced_debug_info)
            + bytes(self.enable_respawn_screen)
            + bytes(self.is_debug)
            + bytes(self.is_flat)
            + bytes(Boolean(self.has_death_location))
            + (bytes(self.death_dimension_name) if self.has_death_location else b"")
            + (bytes(self.death_location) if self.has_death_location else b"")
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (int), is_hardcore (boolean), gamemode (unsigned byte),
        # previous_gamemode (byte), dimensions (list[identifier]),
        # registry_codec (nbt), dimension_type (identifier),
        # dimension_name (identifier), hashed_seed (long), max_players (varint),
        # view_distance (varint), simulation_distance (varint),
        # reduced_debug_info (boolean), enable_respawn_screen (boolean),
        # is_debug (boolean), is_flat (boolean),
        # death_dimension_name (identifier | None), death_location (position | None)
        # entity_id
        entity_id = Int.from_bytes(data)
        # is_hardcore
        is_hardcore = Boolean.from_bytes(data)
        # gamemode
        gamemode = UnsignedByte.from_bytes(data)
        # previous_gamemode
        previous_gamemode = Byte.from_bytes(data)
        # dimensions
        dimensions_size = Varint.from_bytes(data).value
        dimensions = []
        for _ in range(dimensions_size):
            dimensions.append(Identifier.from_bytes(data))
        # registry_codec
        registry_codec = NBT.from_bytes(data)
        # dimension_type
        dimension_type = Identifier.from_bytes(data)
        # dimension_name
        dimension_name = Identifier.from_bytes(data)
        # hashed_seed
        hashed_seed = Long.from_bytes(data)
        # max_players
        max_players = Varint.from_bytes(data)
        # view_distance
        view_distance = Varint.from_bytes(data)
        # simulation_distance
        simulation_distance = Varint.from_bytes(data)
        # reduced_debug_info
        reduced_debug_info = Boolean.from_bytes(data)
        # enable_respawn_screen
        enable_respawn_screen = Boolean.from_bytes(data)
        # is_debug
        is_debug = Boolean.from_bytes(data)
        # is_flat
        is_flat = Boolean.from_bytes(data)
        # death_dimension_name
        has_death_location = Boolean.from_bytes(data).value
        death_dimension_name = (
            Identifier.from_bytes(data) if has_death_location else None
        )
        # death_location
        death_location = Position.from_bytes(data) if has_death_location else None
        return cls(
            entity_id,
            is_hardcore,
            gamemode,
            previous_gamemode,
            dimensions,
            registry_codec,
            dimension_type,
            dimension_name,
            hashed_seed,
            max_players,
            view_distance,
            simulation_distance,
            reduced_debug_info,
            enable_respawn_screen,
            is_debug,
            is_flat,
            death_dimension_name,
            death_location,
        )


class MapDataPacket(Packet):
    """
    Updates a rectangular area on a map item.

    **Packet ID**: ``0x29``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x29
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        map_id: Varint,
        scale: Byte,
        locked: Boolean,
        icons: list[MapIcon],
        updated_columns: UnsignedByte,
        updated_rows: UnsignedByte | None = None,
        x: Byte | None = None,
        z: Byte | None = None,
        data: list[UnsignedByte] | None = None,
    ):
        self.map_id = map_id
        self.scale = scale
        self.locked = locked
        self.icons = icons
        self.updated_columns = updated_columns
        self.updated_rows = updated_rows
        self.x = x
        self.z = z
        self.data = data

    def __bytes__(self):
        res = (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.map_id)
            + bytes(self.scale)
            + bytes(self.locked)
            + bytes(Varint(len(self.icons)))
            + b"".join([bytes(i) for i in self.icons])
            + bytes(self.updated_columns)
        )
        if self.updated_columns.value > 0:
            res += bytes(self.updated_rows)
            res += bytes(self.x)
            res += bytes(self.z)
            res += bytes(Varint(len(self.data)))
            res += b"".join([bytes(i) for i in self.data])
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: map_id (varint), scale (byte), locked (boolean),
        # icons (list[map_icon]), updated_columns (unsigned byte),
        # updated_rows (unsigned byte | None), x (byte | None),
        # z (byte | None), data (list[unsigned byte] | None)
        # map_id
        map_id = Varint.from_bytes(data)
        # scale
        scale = Byte.from_bytes(data)
        # locked
        locked = Boolean.from_bytes(data)
        # icons
        icons_size = Varint.from_bytes(data).value
        icons = []
        for _ in range(icons_size):
            icons.append(MapIcon.from_bytes(data))
        # updated_columns
        updated_columns = UnsignedByte.from_bytes(data)
        if updated_columns:
            # updated_rows
            updated_rows = UnsignedByte.from_bytes(data)
            # x
            x = Byte.from_bytes(data)
            # z
            z = Byte.from_bytes(data)
            # data
            data_size = Varint.from_bytes(data).value
            data = []
            for _ in range(data_size):
                data.append(UnsignedByte.from_bytes(data))
        else:
            updated_rows = None
            x = None
            z = None
            data = None
        return cls(
            map_id, scale, locked, icons, updated_columns, updated_rows, x, z, data
        )


class MerchantOffers(Packet):
    """
    The list of trades a villager NPC is offering.

    **Packet ID**: ``0x2A``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x2A
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        window_id: Varint,
        trades: list[Trade],
        villager_level: Varint,
        experience: Varint,
        is_regular_villager: Boolean,
        can_restock: Boolean,
    ):
        self.window_id = window_id
        self.trades = trades
        self.villager_level = villager_level
        self.experience = experience
        self.is_regular_villager = is_regular_villager
        self.can_restock = can_restock

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(Varint(len(self.trades)))
            + b"".join([bytes(i) for i in self.trades])
            + bytes(self.villager_level)
            + bytes(self.experience)
            + bytes(self.is_regular_villager)
            + bytes(self.can_restock)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (varint), trades (list[trade]),
        # villager_level (varint), experience (varint),
        # is_regular_villager (boolean), can_restock (boolean)
        # window_id
        window_id = Varint.from_bytes(data)
        # trades
        trades_size = Varint.from_bytes(data).value
        trades = []
        for _ in range(trades_size):
            trades.append(Trade.from_bytes(data))
        # villager_level
        villager_level = Varint.from_bytes(data)
        # experience
        experience = Varint.from_bytes(data)
        # is_regular_villager
        is_regular_villager = Boolean.from_bytes(data)
        # can_restock
        can_restock = Boolean.from_bytes(data)
        return cls(
            window_id,
            trades,
            villager_level,
            experience,
            is_regular_villager,
            can_restock,
        )


class UpdateEntityPosition(Packet):
    """
    This packet is sent by the server when an entity moves less then 8 blocks;
    if an entity moves more than 8 blocks Teleport Entity should be sent instead.

    **Packet ID**: ``0x2B``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x2B
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        delta_x: Short,
        delta_y: Short,
        delta_z: Short,
        on_ground: Boolean,
    ):
        self.entity_id = entity_id
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_z = delta_z
        self.on_ground = on_ground

    @property
    def blocks(self) -> tuple[float, float, float]:
        return (
            self.delta_x.value / (32 * 128),
            self.delta_y.value / (32 * 128),
            self.delta_z.value / (32 * 128),
        )

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.delta_x)
            + bytes(self.delta_y)
            + bytes(self.delta_z)
            + bytes(self.on_ground)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), delta_x (short), delta_y (short),
        # delta_z (short), on_ground (boolean)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # delta_x
        delta_x = Short.from_bytes(data)
        # delta_y
        delta_y = Short.from_bytes(data)
        # delta_z
        delta_z = Short.from_bytes(data)
        # on_ground
        on_ground = Boolean.from_bytes(data)
        return cls(entity_id, delta_x, delta_y, delta_z, on_ground)


class UpdateEntityPositionAndRotation(Packet):
    """
    This packet is sent by the server when an entity rotates and moves.
    A maximum of 8 blocks can be moved.

    **Packet ID**: ``0x2C``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x2C
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        delta_x: Short,
        delta_y: Short,
        delta_z: Short,
        yaw: Angle,
        pitch: Angle,
        on_ground: Boolean,
    ):
        self.entity_id = entity_id
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_z = delta_z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    @property
    def blocks(self) -> tuple[float, float, float]:
        return (
            self.delta_x.value / (32 * 128),
            self.delta_y.value / (32 * 128),
            self.delta_z.value / (32 * 128),
        )

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.delta_x)
            + bytes(self.delta_y)
            + bytes(self.delta_z)
            + bytes(self.yaw)
            + bytes(self.pitch)
            + bytes(self.on_ground)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), delta_x (short), delta_y (short),
        # delta_z (short), yaw (angle), pitch (angle), on_ground (boolean)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # delta_x
        delta_x = Short.from_bytes(data)
        # delta_y
        delta_y = Short.from_bytes(data)
        # delta_z
        delta_z = Short.from_bytes(data)
        # yaw
        yaw = Angle.from_bytes(data)
        # pitch
        pitch = Angle.from_bytes(data)
        # on_ground
        on_ground = Boolean.from_bytes(data)
        return cls(entity_id, delta_x, delta_y, delta_z, yaw, pitch, on_ground)


class UpdateEntityRotation(Packet):
    """
    This packet is sent by the server when an entity rotates.

    **Packet ID**: ``0x2D``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x2D
    bound_to = "client"
    state = State.PLAY

    def __init__(self, entity_id: Varint, yaw: Angle, pitch: Angle, on_ground: Boolean):
        self.entity_id = entity_id
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.yaw)
            + bytes(self.pitch)
            + bytes(self.on_ground)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), yaw (angle), pitch (angle),
        # on_ground (boolean)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # yaw
        yaw = Angle.from_bytes(data)
        # pitch
        pitch = Angle.from_bytes(data)
        # on_ground
        on_ground = Boolean.from_bytes(data)
        return cls(entity_id, yaw, pitch, on_ground)


class MoveVehicle(Packet):
    """
    This packet is sent by the server when a vehicle moves.

    **Packet ID**: ``0x2E``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x2E
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        x: Double,
        y: Double,
        z: Double,
        yaw: Angle,
        pitch: Angle,
    ):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.yaw)
            + bytes(self.pitch)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), x (double), y (double), z (double),
        # yaw (angle), pitch (angle)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # x
        x = Double.from_bytes(data)
        # y
        y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # yaw
        yaw = Angle.from_bytes(data)
        # pitch
        pitch = Angle.from_bytes(data)
        return cls(entity_id, x, y, z, yaw, pitch)


class OpenBook(Packet):
    """
    Sent when a player right clicks with a signed book.
    This tells the client to open the book GUI.

    **Packet ID**: ``0x2F``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x2F
    bound_to = "client"
    state = State.PLAY

    def __init__(self, hand: Hand):
        self.hand = hand

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.hand)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: hand (hand)
        # hand
        hand = Hand.from_value(Varint.from_bytes(data))
        return cls(hand)


class OpenScreen(Packet):
    """
    This is sent to the client when it should open an inventory,
    such as a chest, workbench, furnace, or other container.

    **Packet ID**: ``0x30``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x30
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        window_id: Varint,
        window_type: Varint,
        window_title: Chat,
    ):
        self.window_id = window_id
        self.window_type = window_type
        self.window_title = window_title

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(self.window_type)
            + bytes(self.window_title)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (varint), window_type (varint), window_title
        # (chat)
        # window_id
        window_id = Varint.from_bytes(data)
        # window_type
        window_type = Varint.from_bytes(data)
        # window_title
        window_title = Chat.from_bytes(data)
        return cls(window_id, window_type, window_title)


class OpenSignEditor(Packet):
    """
    Sent when the client has placed a sign and is allowed to send Update Sign.

    **Packet ID**: ``0x31``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x31
    bound_to = "client"
    state = State.PLAY

    def __init__(self, location: Position):
        self.location: Position = location

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.location)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: location (position)
        # location
        location = Position.from_bytes(data)
        return cls(location)


class Ping(Packet):
    """
    An unused packet by the default server.
    The client should respond with a Pong when recieved.

    **Packet ID**: ``0x32``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x32
    bound_to = "client"
    state = State.PLAY

    def __init__(self, id: Int):
        self.id = id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.id)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: id (long)
        # id
        id = Int.from_bytes(data)
        return cls(id)


class PlaceGhostRecipe(Packet):
    """
    Sent when the client has placed a ghost recipe in a crafting table.

    **Packet ID**: ``0x33``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x33
    bound_to = "client"
    state = State.PLAY

    def __init__(self, window_id: Varint, recipe_id: Identifier):
        self.window_id = window_id
        self.recipe_id = recipe_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(self.recipe_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (varint), recipe (identifier)
        # window_id
        window_id = Varint.from_bytes(data)
        # recipe
        recipe = Identifier.from_bytes(data)
        return cls(window_id, recipe)


class ClientPlayerAbilities(Packet):
    """
    This packet is sent by the server to update the client's
    abilities and flags.

    **Packet ID**: ``0x34``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x34
    bound_to = "client"
    state = State.PLAY

    def __init__(self, flags: Byte, flying_speed: Float, field_of_view_modifier: Float):
        self.flags = flags
        self.flying_speed = flying_speed
        self.field_of_view_modifier = field_of_view_modifier

    @property
    def invulnerable(self) -> bool:
        return bool(self.flags.value & 0x01)

    @property
    def flying(self) -> bool:
        return bool(self.flags.value & 0x02)

    @property
    def allow_flying(self) -> bool:
        return bool(self.flags.value & 0x04)

    @property
    def creative_mode(self) -> bool:
        return bool(self.flags.value & 0x08)

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.flags)
            + bytes(self.flying_speed)
            + bytes(self.field_of_view_modifier)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: flags (byte), flying_speed (float), field_of_view_modifier
        # (float)
        # flags
        flags = Byte.from_bytes(data)
        # flying_speed
        flying_speed = Float.from_bytes(data)
        # field_of_view_modifier
        field_of_view_modifier = Float.from_bytes(data)
        return cls(flags, flying_speed, field_of_view_modifier)


class PlayerChatMessage(Packet):
    """
    Sends the client a message from a player.

    **Packet ID**: ``0x35``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Server
    """

    packet_id = 0x35
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        header: _DataProxy,
        body: _DataProxy,
        previous_messages: list[_DataProxy],
        other: _DataProxy,
        network_target: _DataProxy,
    ):
        self.header = header
        self.body = body
        self.previous_messages = previous_messages
        self.other = other
        self.network_target = network_target

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.header.sender)
            + bytes(self.header.index)
            + bytes(Boolean(self.header.message_signature is not None))
            + (
                bytes(self.header.message_signature)
                if self.header.message_signature is not None
                else b""
            )
            + bytes(self.body.body)
            + bytes(self.body.timestamp)
            + bytes(self.body.salt)
            + bytes(Varint(len(self.previous_messages)))
            + b"".join(bytes(msg) for msg in self.previous_messages)
            + bytes(self.other.unsigned_content)
            + bytes(Varint(self.other.filter_type.value))
            + (
                bytes(self.other.filter_bits)
                if self.other.filter_bits is not None
                else b""
            )
            + bytes(Varint(self.network_target.chat_type.value))
            + bytes(self.network_target.network_name)
            + bytes(Boolean(self.network_target.network_target_name is not None))
            + (
                bytes(self.network_target.network_target_name)
                if self.network_target.network_target_name is not None
                else b""
            )
        )

    sig_len = 256

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields:
        # - Header
        # sender (uuid), index (varint), message_signature (byte array),
        # - Body
        # body (message), timestamp (long), salt (long),
        # - Previous Messages
        # previous_messages (array[message id, signature]),
        # - Other
        # unsigned_content: (chat), filter_type (enum varint), filter_bits (bit set | None),
        # - Network Target
        # chat_type (varint), network_name (chat), network_target_name_present (bool),
        # network_target_name (chat | None)

        # - Header
        # sender
        sender = UUID.from_bytes(data)
        # index
        index = Varint.from_bytes(data)
        # message_signature
        sig_present = Boolean.from_bytes(data)
        message_signature = None
        if sig_present:
            message_signature = ByteArray.from_bytes(data, length=256)
        header_section = _DataProxy(
            sender=sender,
            index=index,
            message_signature=message_signature,
        )
        # - Body
        # body
        body = String.from_bytes(data)
        # timestamp
        timestamp = Long.from_bytes(data)
        # salt
        salt = Long.from_bytes(data)
        body_section = _DataProxy(
            body=body,
            timestamp=timestamp,
            salt=salt,
        )
        # - Previous Messages
        # previous_messages
        prev_count = Varint.from_bytes(data).value
        previous_messages = []
        for _ in range(prev_count):
            prev_id = Varint.from_bytes(data).value
            prev_sig = ByteArray.from_bytes(data, length=256)
            previous_messages.append(_DataProxy(id=prev_id, signature=prev_sig))
        # - Other
        # unsigned_content
        unsigned_content_present = Boolean.from_bytes(data)
        unsigned_content = Chat.from_bytes(data) if unsigned_content_present else None
        # filter_type
        filter_type = FilterType.from_value(Varint.from_bytes(data))
        # filter_bits
        filter_bits = (
            BitSet.from_bytes(data)
            if filter_type is FilterType.PARTIALLY_FILTERED
            else None
        )
        other_section = _DataProxy(
            unsigned_content=unsigned_content,
            filter_type=filter_type,
            filter_bits=filter_bits,
        )
        # - Network Target
        # chat_types
        chat_type = Varint.from_bytes(data)
        # network_name
        network_name = Chat.from_bytes(data)
        # network_target_name
        network_target_name_present = Boolean.from_bytes(data)
        network_target_name = (
            Chat.from_bytes(data) if network_target_name_present else None
        )
        network_target_section = _DataProxy(
            chat_type=chat_type,
            network_name=network_name,
            network_target_name=network_target_name,
        )
        return cls(
            header=header_section,
            body=body_section,
            previous_messages=previous_messages,
            other=other_section,
            network_target=network_target_section,
        )


class EndCombat(Packet):
    """
    Unused by the default client.

    **Packet ID**: ``0x36``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x36
    bound_to = "client"
    state = State.PLAY

    def __init__(self, duration: Int, entity_id: Varint):
        self.duration = duration
        self.entity_id = entity_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.duration)
            + bytes(self.entity_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: duration (int), entity_id (varint)
        # duration
        duration = Int.from_bytes(data)
        # entity_id
        entity_id = Varint.from_bytes(data)
        return cls(duration, entity_id)


class EnterCombat(Packet):
    """
    Unused by the default client.

    **Packet ID**: ``0x37``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x37
    bound_to = "client"
    state = State.PLAY


class CombatDeath(Packet):
    """
    Used to send a respawn screen.

    **Packet ID**: ``0x38``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x38
    bound_to = "client"
    state = State.PLAY

    def __init__(self, player_id: Varint, entity_id: Int, message: Chat):
        self.player_id = player_id
        self.entity_id = entity_id
        self.message = message

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.player_id)
            + bytes(self.entity_id)
            + bytes(self.message)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: player_id (varint), entity_id (int), message (chat)
        # player_id
        player_id = Varint.from_bytes(data)
        # entity_id
        entity_id = Int.from_bytes(data)
        # message
        message = Chat.from_bytes(data)
        return cls(player_id, entity_id, message)


class PlayerInfoRemove(Packet):
    """
    Used by the server to remove players from the player list.

    **Packet ID**: ``0x39``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x39
    bound_to = "client"
    state = State.PLAY

    def __init__(self, players: list[UUID]):
        self.players = players

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(Varint(len(self.players)))
            + b"".join([bytes(p) for p in self.players])
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: players (list of UUID)
        # players
        player_count = Varint.from_bytes(data).value
        players = []
        for _ in range(player_count):
            players.append(UUID.from_bytes(data))
        return cls(players)


class PlayerInfoUpdate(Packet):
    """
    Sent by the server to update the user list (<tab> in the client).

    **Packet ID**: ``0x3A``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x3A
    bound_to = "client"
    state = State.PLAY

    def __init__(self, actions: Byte, players: list[PlayerInfoUpdatePlayer]):
        self.actions = actions
        self.players = players

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.actions)
            + bytes(Varint(len(self.players)))
            + b"".join(bytes(player) for player in self.players)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: actions (byte), players (list of player info)
        # actions
        actions = Byte.from_bytes(data)
        # players
        player_count = Varint.from_bytes(data).value
        players = []
        for _ in range(player_count):
            players.append(PlayerInfoUpdatePlayer.from_bytes(data, actions))
        return cls(actions, players)


class LookAt(Packet):
    """
    Used to change the player's look direction.

    **Packet ID**: ``0x3B``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x3B
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        feet_eyes: FeetEyes,
        target_x: Double,
        target_y: Double,
        target_z: Double,
        is_entity: Boolean,
        entity_id: Varint | None,
        entity_feet_eyes: FeetEyes | None,
    ):
        self.feet_eyes = feet_eyes
        self.target_x = target_x
        self.target_y = target_y
        self.target_z = target_z
        self.is_entity = is_entity
        self.entity_id = entity_id
        self.entity_feet_eyes = entity_feet_eyes

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.feet_eyes)
            + bytes(self.target_x)
            + bytes(self.target_y)
            + bytes(self.target_z)
            + bytes(self.is_entity)
            + bytes(self.entity_id)
            + bytes(self.entity_feet_eyes)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: feet_eyes (varint), target_x (double), target_y (double), target_z (double),
        # is_entity (boolean), entity_id (varint), entity_feet_eyes (varint)
        # feet_eyes
        feet_eyes = FeetEyes.from_value(Varint.from_bytes(data))
        # target_x
        target_x = Double.from_bytes(data)
        # target_y
        target_y = Double.from_bytes(data)
        # target_z
        target_z = Double.from_bytes(data)
        # is_entity
        is_entity = Boolean.from_bytes(data)
        # entity_id
        entity_id = Varint.from_bytes(data) if is_entity else None
        # entity_feet_eyes
        entity_feet_eyes = (
            FeetEyes.from_value(Varint.from_bytes(data)) if is_entity else None
        )
        return cls(
            feet_eyes,
            target_x,
            target_y,
            target_z,
            is_entity,
            entity_id,
            entity_feet_eyes,
        )


class SynchronizePlayerPosition(Packet):
    """
    Used to synchronize the player's position with the server.

    **Packet ID**: ``0x3C``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x3C
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        x: Double,
        y: Double,
        z: Double,
        feet_eyes: FeetEyes,
        flags: Byte,
        teleport_id: Varint,
    ):
        self.x = x
        self.y = y
        self.z = z
        self.feet_eyes = feet_eyes
        self.flags = flags
        self.teleport_id = teleport_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.feet_eyes)
            + bytes(self.flags)
            + bytes(self.teleport_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: x (double), y (double), z (double), feet_eyes (varint), flags (byte),
        # teleport_id (varint), dismount_vehicle (boolean)
        # x
        x = Double.from_bytes(data)
        # y
        y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # feet_eyes
        feet_eyes = FeetEyes.from_value(Varint.from_bytes(data))
        # flags
        flags = Byte.from_bytes(data)
        # teleport_id
        teleport_id = Varint.from_bytes(data)
        # dismount_vehicle
        dismount_vehicle = Boolean.from_bytes(data)
        return cls(x, y, z, feet_eyes, flags, teleport_id, dismount_vehicle)


class UpdateRecipeBook(Packet):
    """
    Used to update the recipe book.

    **Packet ID**: ``0x3D``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x3D
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        action: RecipeBookActionType,
        crafting_recipe_book_open: Boolean,
        crafting_recipe_book_filter_active: Boolean,
        smelting_recipe_book_open: Boolean,
        smelting_recipe_book_filter_active: Boolean,
        blast_furnace_recipe_book_open: Boolean,
        blast_furnace_recipe_book_filter_active: Boolean,
        smoker_recipe_book_open: Boolean,
        smoker_recipe_book_filter_active: Boolean,
        array_1: list[Identifier],
        array_2: list[Identifier],
    ):
        self.action = action
        self.crafting_recipe_book_open = crafting_recipe_book_open
        self.crafting_recipe_book_filter_active = crafting_recipe_book_filter_active
        self.smelting_recipe_book_open = smelting_recipe_book_open
        self.smelting_recipe_book_filter_active = smelting_recipe_book_filter_active
        self.blast_furnace_recipe_book_open = blast_furnace_recipe_book_open
        self.blast_furnace_recipe_book_filter_active = (
            blast_furnace_recipe_book_filter_active
        )
        self.smoker_recipe_book_open = smoker_recipe_book_open
        self.smoker_recipe_book_filter_active = smoker_recipe_book_filter_active
        self.array_1 = array_1
        self.array_2 = array_2

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.action)
            + bytes(self.crafting_recipe_book_open)
            + bytes(self.crafting_recipe_book_filter_active)
            + bytes(self.smelting_recipe_book_open)
            + bytes(self.smelting_recipe_book_filter_active)
            + bytes(self.blast_furnace_recipe_book_open)
            + bytes(self.blast_furnace_recipe_book_filter_active)
            + bytes(self.smoker_recipe_book_open)
            + bytes(self.smoker_recipe_book_filter_active)
            + bytes(Varint(len(self.array_1)))
            + b"".join(bytes(x) for x in self.array_1)
            + bytes(Varint(len(self.array_2)))
            if self.array_2 is not None
            else b"" + b"".join(bytes(x) for x in self.array_2)
            if self.array_2 is not None
            else b""
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: action (varint), crafting_recipe_book_open (boolean),
        # crafting_recipe_book_filter_active (boolean), smelting_recipe_book_open (boolean),
        # smelting_recipe_book_filter_active (boolean), blast_furnace_recipe_book_open (boolean),
        # blast_furnace_recipe_book_filter_active (boolean), smoker_recipe_book_open (boolean),
        # smoker_recipe_book_filter_active (boolean), array_1 (varint, identifier[]),
        # array_2 (varint, identifier[])
        # action
        action = RecipeBookActionType.from_value(Varint.from_bytes(data))
        # crafting_recipe_book_open
        crafting_recipe_book_open = Boolean.from_bytes(data)
        # crafting_recipe_book_filter_active
        crafting_recipe_book_filter_active = Boolean.from_bytes(data)
        # smelting_recipe_book_open
        smelting_recipe_book_open = Boolean.from_bytes(data)
        # smelting_recipe_book_filter_active
        smelting_recipe_book_filter_active = Boolean.from_bytes(data)
        # blast_furnace_recipe_book_open
        blast_furnace_recipe_book_open = Boolean.from_bytes(data)
        # blast_furnace_recipe_book_filter_active
        blast_furnace_recipe_book_filter_active = Boolean.from_bytes(data)
        # smoker_recipe_book_open
        smoker_recipe_book_open = Boolean.from_bytes(data)
        # smoker_recipe_book_filter_active
        smoker_recipe_book_filter_active = Boolean.from_bytes(data)
        # array_1
        array_1 = []
        for _ in range(Varint.from_bytes(data).value):
            array_1.append(Identifier.from_bytes(data))
        # array_2
        array_2 = None
        if action.value == 0:
            array_2 = []
            for _ in range(Varint.from_bytes(data).value):
                array_2.append(Identifier.from_bytes(data))
        return cls(
            action,
            crafting_recipe_book_open,
            crafting_recipe_book_filter_active,
            smelting_recipe_book_open,
            smelting_recipe_book_filter_active,
            blast_furnace_recipe_book_open,
            blast_furnace_recipe_book_filter_active,
            smoker_recipe_book_open,
            smoker_recipe_book_filter_active,
            array_1,
            array_2,
        )


class RemoveEntities(Packet):
    """
    Sent by the server when an entity is to be destroyed on the client.

    **Packet ID**: ``0x3E``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x3E
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_ids: list[Varint],
    ):
        self.entity_ids = entity_ids

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(Varint(len(self.entity_ids)))
            + b"".join(bytes(x) for x in self.entity_ids)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_ids (varint, varint[])
        # entity_ids
        entity_ids = []
        for _ in range(Varint.from_bytes(data).value):
            entity_ids.append(Varint.from_bytes(data))
        return cls(entity_ids)


class RemoveEntityEffect(Packet):
    """
    Sent by the server when an entity effect is to be removed from an entity.

    **Packet ID**: ``0x3F``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x3F
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        effect_id: Varint,
    ):
        self.entity_id = entity_id
        self.effect_id = effect_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.effect_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), effect_id (varint)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # effect_id
        effect_id = Varint.from_bytes(data)
        return cls(entity_id, effect_id)


class ResourcePack(Packet):
    """
    Sent by the server when a resource pack is to be sent to the client.

    **Packet ID**: ``0x40``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x40
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        url: String,
        hash: String,
        forced: Boolean,
        prompt_message: String | None,
    ):
        self.url = url
        self.hash = hash
        self.forced = forced
        self.prompt_message = prompt_message

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.url)
            + bytes(self.hash)
            + bytes(self.forced)
            + bytes(Boolean(self.prompt_message is not None))
            + (bytes(self.prompt_message) if self.prompt_message is not None else b"")
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: url (string), hash (string), forced (boolean),
        # prompt_message (boolean, string)
        # url
        url = String.from_bytes(data, max_length=32767)
        # hash
        hash = String.from_bytes(data, max_length=40)
        # forced
        forced = Boolean.from_bytes(data)
        # prompt_message
        prompt_message = None
        if Boolean.from_bytes(data):
            prompt_message = String.from_bytes(data)
        return cls(url, hash, forced, prompt_message)


class Respawn(Packet):
    """
    To change the player's dimension (overworld/nether/end),
    send them a respawn packet with the appropriate dimension,
    followed by prechunks/chunks for the new dimension,
    and finally a position and look packet.
    You do not need to unload chunks, the client will do it automatically.

    **Packet ID**: ``0x41``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x41
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        dimension_type: Identifier,
        dimension_name: Identifier,
        hashed_seed: Long,
        gamemode: UnsignedByte,
        previous_gamemode: Byte,
        is_debug: Boolean,
        is_flat: Boolean,
        copy_metadata: Boolean,
        has_death_location: Boolean,
        death_dimension: Identifier | None = None,
        death_location: Position | None = None,
    ):
        self.dimension_type = dimension_type
        self.dimension_name = dimension_name
        self.hashed_seed = hashed_seed
        self.gamemode = gamemode
        self.previous_gamemode = previous_gamemode
        self.is_debug = is_debug
        self.is_flat = is_flat
        self.copy_metadata = copy_metadata
        self.has_death_location = has_death_location
        self.death_dimension = death_dimension
        self.death_location = death_location

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.dimension_type)
            + bytes(self.dimension_name)
            + bytes(self.hashed_seed)
            + bytes(self.gamemode)
            + bytes(self.previous_gamemode)
            + bytes(self.is_debug)
            + bytes(self.is_flat)
            + bytes(self.copy_metadata)
            + bytes(self.has_death_location)
            + (bytes(self.death_dimension) if self.has_death_location else b"")
            + (bytes(self.death_location) if self.has_death_location else b"")
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: dimension_type (identifier), dimension_name (identifier),
        # hashed_seed (long), gamemode (unsigned byte), previous_gamemode (byte),
        # is_debug (boolean), is_flat (boolean), copy_metadata (boolean),
        # has_death_location (boolean), death_dimension (identifier),
        # death_location (position)
        # dimension_type
        dimension_type = Identifier.from_bytes(data)
        # dimension_name
        dimension_name = Identifier.from_bytes(data)
        # hashed_seed
        hashed_seed = Long.from_bytes(data)
        # gamemode
        gamemode = UnsignedByte.from_bytes(data)
        # previous_gamemode
        previous_gamemode = Byte.from_bytes(data)
        # is_debug
        is_debug = Boolean.from_bytes(data)
        # is_flat
        is_flat = Boolean.from_bytes(data)
        # copy_metadata
        copy_metadata = Boolean.from_bytes(data)
        # has_death_location
        has_death_location = Boolean.from_bytes(data)
        # death_dimension
        death_dimension = None
        if has_death_location:
            death_dimension = Identifier.from_bytes(data)
        # death_location
        death_location = None
        if has_death_location:
            death_location = Position.from_bytes(data)
        return cls(
            dimension_type,
            dimension_name,
            hashed_seed,
            gamemode,
            previous_gamemode,
            is_debug,
            is_flat,
            copy_metadata,
            has_death_location,
            death_dimension,
            death_location,
        )


class SetHeadRotation(Packet):
    """
    Changes the direction an entity's head is facing.

    **Packet ID**: ``0x42``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x42
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        head_yaw: Angle,
    ):
        self.entity_id = entity_id
        self.head_yaw = head_yaw

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.head_yaw)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), head_yaw (angle)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # head_yaw
        head_yaw = Angle.from_bytes(data)
        return cls(entity_id, head_yaw)


class UpdateSectionBlocks(Packet):
    """
    Sent whenever 2 or more blocks are changed within the same chunk on the same tick.

    **Packet ID**: ``0x43``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x43
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        chunk_section_position: Long,
        suppress_light_updates: Boolean,
        blocks: list[Varlong],
    ):
        self.chunk_section_position = chunk_section_position
        self.suppress_light_updates = suppress_light_updates
        self.blocks = blocks

    @property
    def chunk_x(self):
        return self.chunk_section_position.value >> 42

    @property
    def chunk_y(self):
        return self.chunk_section_position.value << 44 >> 44

    @property
    def chunk_z(self):
        return self.chunk_section_position.value << 22 >> 42

    def parse_blocks(self) -> Generator[tuple[int, int, int, int], None, None]:
        for block in self.blocks:
            block_state_id = block.value >> 12
            block_local_x = block.value << 52 >> 56
            block_local_z = block.value << 48 >> 60
            block_local_y = block.value << 44 >> 60
            yield block_state_id, block_local_x, block_local_y, block_local_z

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.chunk_section_position)
            + bytes(self.suppress_light_updates)
            + bytes(Varint(len(self.blocks)))
            + b"".join(bytes(block) for block in self.blocks)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: chunk_section_position (long), suppress_light_updates (boolean),
        # blocks (varlong[])
        # chunk_section_position
        chunk_section_position = Long.from_bytes(data)
        # suppress_light_updates
        suppress_light_updates = Boolean.from_bytes(data)
        # blocks
        blocks = []
        for _ in range(Varint.from_bytes(data).value):
            blocks.append(Varlong.from_bytes(data))
        return cls(chunk_section_position, suppress_light_updates, blocks)


class SelectAdvancementsTab(Packet):
    """
    Sent by the server to indicate that the client should switch advancement tab.
    Sent either when the client switches tab in the GUI or when an advancement in another tab is made.

    **Packet ID**: ``0x44``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x44
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        has_tab: Boolean,
        tab_id: Identifier,
    ):
        self.has_tab = has_tab
        self.tab_id = tab_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.has_tab)
            + (bytes(self.tab_id) if self.has_tab else b"")
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: has_tab (boolean), tab_id (identifier)
        # has_tab
        has_tab = Boolean.from_bytes(data)
        # tab_id
        tab_id = None
        if has_tab:
            tab_id = Identifier.from_bytes(data)
        return cls(has_tab, tab_id)


class ServerData(Packet):
    """
    Sent by the server to the client to send information about the server.

    **Packet ID**: ``0x45``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x45
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        motd: Chat,
        icon: String | None = None,
        enforces_secure_chat: Boolean = Boolean(False),
    ):
        self.motd = motd
        self.icon = icon
        self.enforces_secure_chat = enforces_secure_chat

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.motd)
            + bytes(Boolean(self.icon is not None))
            + (bytes(self.icon) if self.icon is not None else b"")
            + bytes(self.enforces_secure_chat)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: motd (chat), icon (string), enforces_secure_chat (boolean)
        # motd
        motd = Chat.from_bytes(data)
        # icon
        icon = None
        if Boolean.from_bytes(data).value:
            icon = String.from_bytes(data, max_length=32767)
        # enforces_secure_chat
        enforces_secure_chat = Boolean.from_bytes(data)
        return cls(motd, icon, enforces_secure_chat)


class SetActionBarText(Packet):
    """
    Sent by the server to the client to set the action bar text.
    The action bar text is displayed as a message above the hotbar.

    **Packet ID**: ``0x46``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x46
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        text: Chat,
    ):
        self.text = text

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.text)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: text (chat)
        # text
        text = Chat.from_bytes(data)
        return cls(text)


class SetBorderCenter(Packet):
    """
    Sent by the server to the client to set the center of the world border.

    **Packet ID**: ``0x47``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x47
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        x: Double,
        z: Double,
    ):
        self.x = x
        self.z = z

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.x) + bytes(self.z)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: x (double), z (double)
        # x
        x = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        return cls(x, z)


class SetBorderLerpSize(Packet):
    """
    Sent by the server to the client to set the size of the world border.

    **Packet ID**: ``0x48``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x48
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        old_diameter: Double,
        new_diameter: Double,
        speed: Varlong,
    ):
        self.old_diameter = old_diameter
        self.new_diameter = new_diameter
        self.speed = speed

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.old_diameter)
            + bytes(self.new_diameter)
            + bytes(self.speed)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: old_diameter (double), new_diameter (double), speed (varlong)
        # old_diameter
        old_diameter = Double.from_bytes(data)
        # new_diameter
        new_diameter = Double.from_bytes(data)
        # speed
        speed = Varlong.from_bytes(data)
        return cls(old_diameter, new_diameter, speed)


class SetBorderSize(Packet):
    """
    Sent by the server to the client to set the size of the world border.

    **Packet ID**: ``0x49``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x49
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        diameter: Double,
    ):
        self.diameter = diameter

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.diameter)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: diameter (double)
        # diameter
        diameter = Double.from_bytes(data)
        return cls(diameter)


class SetBorderWarningDelay(Packet):
    """
    Sent by the server to the client to set the warning delay of the world border.

    **Packet ID**: ``0x4A``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x4A
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        delay: Varint,
    ):
        self.delay = delay

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.delay)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: delay (varint)
        # delay
        delay = Varint.from_bytes(data)
        return cls(delay)


class SetBorderWarningDistance(Packet):
    """
    Sent by the server to the client to set the warning distance of the world border.

    **Packet ID**: ``0x4B``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x4B
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        distance: Varint,
    ):
        self.distance = distance

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.distance)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: distance (varint)
        # distance
        distance = Varint.from_bytes(data)
        return cls(distance)


class SetCamera(Packet):
    """
    Sets the entity that the player renders from.
    This is normally used when the player left-clicks an entity while in spectator mode.

    **Packet ID**: ``0x4C``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x4C
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
    ):
        self.entity_id = entity_id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.entity_id)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint)
        # entity_id
        entity_id = Varint.from_bytes(data)
        return cls(entity_id)


class ClientSetHeldItem(Packet):
    """
    Sent by the server to the client to set the held item of the player.

    **Packet ID**: ``0x4D``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x4D
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        slot: Byte,
    ):
        self.slot = slot

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.slot)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: slot (byte)
        # slot
        slot = Byte.from_bytes(data)
        return cls(slot)


class SetCenterChunk(Packet):
    """
    Updates the client's location.
    This is used to determine what chunks should remain loaded and if a
    chunk load should be ignored; chunks outside of the view distance may be unloaded.

    Sent whenever the player moves across a chunk border horizontally,
    and also (according to testing) for any integer change in the vertical axis,
    even if it doesn't go across a chunk section border.

    **Packet ID**: ``0x4E``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x4E
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        chunk_x: Varint,
        chunk_z: Varint,
    ):
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.chunk_x)
            + bytes(self.chunk_z)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: chunk_x (varint), chunk_z (varint)
        # chunk_x
        chunk_x = Varint.from_bytes(data)
        # chunk_z
        chunk_z = Varint.from_bytes(data)
        return cls(chunk_x, chunk_z)


class SetRenderDistance(Packet):
    """
    Sent by the integrated singleplayer server when changing render distance.
    This packet is sent by the server when the client reappears in the overworld after leaving the end.

    **Packet ID**: ``0x4F``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x4F
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        distance: Varint,
    ):
        self.distance = distance

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.distance)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: distance (varint)
        # distance
        distance = Varint.from_bytes(data)
        return cls(distance)


class SetDefaultSpawnLocation(Packet):
    """
    Sent by the server after login to specify the coordinates of the spawn point
    (the point at which players spawn at, and which the compass points to).
    It can be sent at any time to update the point compasses point at.

    **Packet ID**: ``0x50``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x50
    bound_to = "client"
    state = State.PLAY

    def __init__(self, location: Position, angle: Float):
        self.location = location
        self.angle = angle

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") + bytes(self.location) + bytes(self.angle)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: location (position), angle (float)
        # location
        location = Position.from_bytes(data)
        # angle
        angle = Float.from_bytes(data)
        return cls(location, angle)


class DisplayObjective(Packet):
    """
    Sent by the server to the client to display an objective on the scoreboard.

    **Packet ID**: ``0x51``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x51
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        position: ScoreboardPosition,
        objective_name: String,
    ):
        self.position = position
        self.objective_name = objective_name

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.position.value)
            + bytes(self.objective_name)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: position (scoreboard_position), objective_name (string)
        # position
        position = ScoreboardPosition.from_value(Byte.from_bytes(data))
        # objective_name
        objective_name = String.from_bytes(data)
        return cls(position, objective_name)


class SetEntityMetadata(Packet):
    """
    Sent by the server to the client to update the metadata of an entity.
    Any properties not included in the Metadata field are left unchanged.

    **Packet ID**: ``0x52``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x52
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        metadata: EntityMetadata,
    ):
        self.entity_id = entity_id
        self.metadata = metadata

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.metadata)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), metadata (metadata)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # metadata
        metadata = EntityMetadata.from_bytes(data)
        return cls(entity_id, metadata)


class LinkEntities(Packet):
    """
    Sent by the server to the client to link two entities together.
    This is used to link a leash to a mob and the player holding it.

    **Packet ID**: ``0x53``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x53
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        attached_entity_id: Int,
        holding_entity_id: Int,
    ):
        self.attached_entity_id = attached_entity_id
        self.holding_entity_id = holding_entity_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.attached_entity_id)
            + bytes(self.holding_entity_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: attached_entity_id (int), holding_entity_id (int)
        # attached_entity_id
        attached_entity_id = Int.from_bytes(data)
        # holding_entity_id
        holding_entity_id = Int.from_bytes(data)
        return cls(attached_entity_id, holding_entity_id)


class SetEntityVelocity(Packet):
    """
    Sent by the server to the client to update the velocity of an entity.

    Velocity is believed to be in units of 1/8000 of a block per server tick (50ms);
    for example, -1343 would move (-1343 / 8000) = ~0.167875 blocks per tick (or ~3.3575 blocks per second).

    **Packet ID**: ``0x54``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x54
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        velocity_x: Short,
        velocity_y: Short,
        velocity_z: Short,
    ):
        self.entity_id = entity_id
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.velocity_z = velocity_z

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.velocity_x)
            + bytes(self.velocity_y)
            + bytes(self.velocity_z)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), velocity_x (short), velocity_y (short), velocity_z (short)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # velocity_x
        velocity_x = Short.from_bytes(data)
        # velocity_y
        velocity_y = Short.from_bytes(data)
        # velocity_z
        velocity_z = Short.from_bytes(data)
        return cls(entity_id, velocity_x, velocity_y, velocity_z)


class SetEquipment(Packet):
    """
    Sent by the server to the client to update the equipment of an entity.

    **Packet ID**: ``0x55``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x55
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        equipment: list[tuple[Byte, Slot]],
    ):
        self.entity_id = entity_id
        self.equipment = equipment

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + b"".join(bytes(slot) + bytes(item) for slot, item in self.equipment)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), equipment (Array[(slot byte), (item slot)])
        # entity_id
        entity_id = Varint.from_bytes(data)
        # equipment
        equipment = []
        for _ in range(5):
            slot = Byte.from_bytes(data)
            item = Slot.from_bytes(data)
            equipment.append((slot, item))
            if slot.value & 0x80 == 0:
                break
        return cls(entity_id, equipment)


class SetExperience(Packet):
    """
    Sent by the server when the client should change XP levels.

    **Packet ID**: ``0x56``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x56
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        experience_bar: Float,
        total_experience: Varint,
        level: Varint,
    ):
        self.experience_bar = experience_bar
        self.total_experience = total_experience
        self.level = level

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.experience_bar)
            + bytes(self.total_experience)
            + bytes(self.level)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: experience_bar (float), total_experience (varint), level (varint)
        # experience_bar
        experience_bar = Float.from_bytes(data)
        # total_experience
        total_experience = Varint.from_bytes(data)
        # level
        level = Varint.from_bytes(data)
        return cls(experience_bar, total_experience, level)


class SetHealth(Packet):
    """
    Sent by the server when the client should change their health.

    **Packet ID**: ``0x57``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x57
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        health: Float,
        food: Varint,
        food_saturation: Float,
    ):
        self.health = health
        self.food = food
        self.food_saturation = food_saturation

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.health)
            + bytes(self.food)
            + bytes(self.food_saturation)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: health (float), food (varint), food_saturation (float)
        # health
        health = Float.from_bytes(data)
        # food
        food = Varint.from_bytes(data)
        # food_saturation
        food_saturation = Float.from_bytes(data)
        return cls(health, food, food_saturation)


class UpdateObjectives(Packet):
    """
    Sent by the server to the client to update the scoreboard objectives.

    **Packet ID**: ``0x58``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x58
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        objective_name: String,
        mode: UpdateObjectiveModes,
        objective_value: Chat | None = None,
        objective_type: UpdateObjectiveType | None = None,
    ):
        self.objective_name = objective_name
        self.mode = mode
        self.objective_value = objective_value
        self.objective_type = objective_type

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.objective_name)
            + bytes(self.mode)
            + bytes(self.objective_value)
            + bytes(self.objective_type)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: objective_name (string), mode (byte), objective_value (chat), objective_type (varint)
        # objective_name
        objective_name = String.from_bytes(data)
        # mode
        mode = UpdateObjectiveModes.from_value(Byte.from_bytes(data))
        # objective_value
        objective_value = (
            Chat.from_bytes(data)
            if mode in (UpdateObjectiveModes.CREATE, UpdateObjectiveModes.UPDATE)
            else None
        )
        # objective_type
        objective_type = (
            UpdateObjectiveType(Varint.from_bytes(data))
            if mode in (UpdateObjectiveModes.CREATE, UpdateObjectiveModes.UPDATE)
            else None
        )
        return cls(objective_name, mode, objective_value, objective_type)


class SetPassengers(Packet):
    """
    Sent by the server to the client to set the passengers of an entity.

    **Packet ID**: ``0x59``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x59
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        passengers: list[Varint],
    ):
        self.entity_id = entity_id
        self.passengers = passengers

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(Varint(len(self.passengers)))
            + b"".join(bytes(passenger) for passenger in self.passengers)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), passengers (array of varints)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # passengers
        passengers = []
        for _ in range(Varint.from_bytes(data).value):
            passengers.append(Varint.from_bytes(data))
        return cls(entity_id, passengers)


class UpdateTeams(Packet):
    """
    Sent by the server to the client to update the scoreboard teams.

    **Packet ID**: ``0x5A``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x5A
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        team_name: String,
        mode: UpdateTeamModes,
        data: _DataProxy,
    ):
        self.team_name = team_name
        self.mode = mode
        self.data = data

    def __bytes__(self):
        res = (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.team_name)
            + bytes(self.mode.value)
        )
        if self.mode is UpdateTeamModes.CREATE:
            res += (
                bytes(self.data.display_name)
                + bytes(self.data.friendly_flags)
                + bytes(self.data.name_tag_visibility)
                + bytes(self.data.collision_rule)
                + bytes(self.data.color)
                + bytes(self.data.prefix)
                + bytes(self.data.suffix)
                + bytes(Varint(len(self.data.entities)))
                + b"".join([bytes(e) for e in self.data.entities])
            )
        elif self.mode is UpdateTeamModes.REMOVE:
            pass
        elif self.mode is UpdateTeamModes.UPDATE:
            res += (
                bytes(self.data.friendly_flags)
                + bytes(self.data.name_tag_visibility)
                + bytes(self.data.collision_rule)
                + bytes(self.data.color)
                + bytes(self.data.prefix)
                + bytes(self.data.suffix)
            )
        elif self.mode in (
            UpdateTeamModes.ADD_ENTITIES,
            UpdateTeamModes.REMOVE_ENTITIES,
        ):
            res += bytes(Varint(len(self.data.entities))) + b"".join(
                [bytes(e) for e in self.data.entities]
            )
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: team_name (string), mode (byte), *data
        # team_name
        team_name = String.from_bytes(data, max_length=16)
        # mode
        mode = UpdateTeamModes.from_value(Byte.from_bytes(data))
        # data
        if mode is UpdateTeamModes.CREATE:
            data = _DataProxy(
                display_name=Chat.from_bytes(data),
                friendly_flags=Byte.from_bytes(data),
                name_tag_visibility=NameTagVisibility(
                    String.from_bytes(data, max_length=32)
                ),
                collision_rule=CollisionRule(String.from_bytes(data, max_length=32)),
                color=ChatColor(Varint.from_bytes(data)),
                prefix=Chat.from_bytes(data),
                suffix=Chat.from_bytes(data),
                entities=[
                    String.from_bytes(data, max_length=40)
                    for _ in range(Varint.from_bytes(data).value)
                ],
            )
        elif mode is UpdateTeamModes.REMOVE:
            data = _DataProxy()
        elif mode is UpdateTeamModes.UPDATE:
            data = _DataProxy(
                display_name=Chat.from_bytes(data),
                friendly_flags=Byte.from_bytes(data),
                name_tag_visibility=NameTagVisibility(
                    String.from_bytes(data, max_length=32)
                ),
                collision_rule=CollisionRule(String.from_bytes(data, max_length=32)),
                color=ChatColor(Varint.from_bytes(data)),
                prefix=Chat.from_bytes(data),
                suffix=Chat.from_bytes(data),
            )
        elif mode in (UpdateTeamModes.ADD_ENTITIES, UpdateTeamModes.REMOVE_ENTITIES):
            data = _DataProxy(
                entities=[
                    String.from_bytes(data, max_length=40)
                    for _ in range(Varint.from_bytes(data).value)
                ]
            )
        else:
            raise ValueError("Invalid mode")
        return cls(team_name, mode, data)


class UpdateScore(Packet):
    """
    Sent by the server to the client to update the scoreboard scores.

    **Packet ID**: ``0x5B``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x5B
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_name: String,
        action: UpdateScoreAction,
        objective_name: String,
        value: Varint | None = None,
    ):
        self.entity_name = entity_name
        self.action = action
        self.objective_name = objective_name
        self.value = value

    def __bytes__(self):
        res = (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_name)
            + bytes(self.action.value)
            + bytes(self.objective_name)
        )
        if self.action is UpdateScoreAction.CREATE_OR_UPDATE:
            res += bytes(self.value)
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_name (string), action (byte), objective_name (string), value (varint)
        # entity_name
        entity_name = String.from_bytes(data, max_length=40)
        # action
        action = UpdateScoreAction.from_value(Varint.from_bytes(data))
        # objective_name
        objective_name = String.from_bytes(data, max_length=16)
        # value
        value = (
            Varint.from_bytes(data)
            if action is UpdateScoreAction.CREATE_OR_UPDATE
            else None
        )
        return cls(entity_name, action, objective_name, value)


class SetSimulationDistance(Packet):
    """
    Sent by the server to the client to set the distance at
    which the client will receive simulation updates.

    **Packet ID**: ``0x5C``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x5C
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        distance: Varint,
    ):
        self.distance = distance

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.distance)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: distance (varint)
        # distance
        distance = Varint.from_bytes(data)
        return cls(distance)


class SetSubtitleText(Packet):
    """
    Sent by the server to the client to set the subtitle text.

    **Packet ID**: ``0x5D``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x5D
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        subtitle: Chat,
    ):
        self.subtitle = subtitle

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.subtitle)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: subtitle (chat)
        # subtitle
        subtitle = Chat.from_bytes(data)
        return cls(subtitle)


class UpdateTime(Packet):
    """
    Time is based on ticks, where 20 ticks happen every second.
    There are 24000 ticks in a day, making Minecraft days exactly 20 minutes long.

    The time of day is based on the timestamp modulo 24000.
    0 is sunrise, 6000 is noon, 12000 is sunset, and 18000 is midnight.

    **Packet ID**: ``0x5E``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x5E
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        world_age: Long,
        time_of_day: Long,
    ):
        self.world_age = world_age
        self.time_of_day = time_of_day

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.world_age)
            + bytes(self.time_of_day)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: world_age (long), time_of_day (long)
        # world_age
        world_age = Long.from_bytes(data)
        # time_of_day
        time_of_day = Long.from_bytes(data)
        return cls(world_age, time_of_day)


class SetTitleText(Packet):
    """
    Sent by the server to the client to set the title text.

    **Packet ID**: ``0x5F``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x5F
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        title: Chat,
    ):
        self.title = title

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.title)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: title (chat)
        # title
        title = Chat.from_bytes(data)
        return cls(title)


class SetTitleAnimationTimes(Packet):
    """
    Sent by the server to the client to set the title animation times.

    **Packet ID**: ``0x60``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x60
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        fade_in: Int,
        stay: Int,
        fade_out: Int,
    ):
        self.fade_in = fade_in
        self.stay = stay
        self.fade_out = fade_out

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.fade_in)
            + bytes(self.stay)
            + bytes(self.fade_out)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: fade_in (int), stay (int), fade_out (int)
        # fade_in
        fade_in = Int.from_bytes(data)
        # stay
        stay = Int.from_bytes(data)
        # fade_out
        fade_out = Int.from_bytes(data)
        return cls(fade_in, stay, fade_out)


class EntitySoundEffect(Packet):
    """
    Sent by the server to the client to play a sound effect
    for an entity.

    **Packet ID**: ``0x61``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x61
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        sound_id: Varint,
        sound_category: Varint,
        entity_id: Varint,
        volume: Float,
        pitch: Float,
        seed: Long,
    ):
        self.sound_id = sound_id
        self.sound_category = sound_category
        self.entity_id = entity_id
        self.volume = volume
        self.pitch = pitch
        self.seed = seed

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.sound_id)
            + bytes(self.sound_category)
            + bytes(self.entity_id)
            + bytes(self.volume)
            + bytes(self.pitch)
            + bytes(self.seed)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: sound_id (varint), sound_category (varint), entity_id (varint), volume (float), pitch (float)
        # sound_id
        sound_id = Varint.from_bytes(data)
        # sound_category
        sound_category = Varint.from_bytes(data)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # volume
        volume = Float.from_bytes(data)
        # pitch
        pitch = Float.from_bytes(data)
        # seed
        seed = Long.from_bytes(data)
        return cls(sound_id, sound_category, entity_id, volume, pitch, seed)


class SoundEffect(Packet):
    """
    Sent by the server to the client to play a sound effect.

    **Packet ID**: ``0x5E``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x62
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        sound_id: Varint,
        sound_category: Varint,
        x: Int,
        y: Int,
        z: Int,
        volume: Float,
        pitch: Float,
        seed: Long,
    ):
        self.sound_id = sound_id
        self.sound_category = sound_category
        self.x = x
        self.y = y
        self.z = z
        self.volume = volume
        self.pitch = pitch
        self.seed = seed

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.sound_id)
            + bytes(self.sound_category)
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.volume)
            + bytes(self.pitch)
            + bytes(self.seed)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: sound_id (varint), sound_category (varint), x (int), y (int), z (int), volume (float), pitch (float)
        # sound_id
        sound_id = Varint.from_bytes(data)
        # sound_category
        sound_category = Varint.from_bytes(data)
        # x
        x = Int.from_bytes(data)
        # y
        y = Int.from_bytes(data)
        # z
        z = Int.from_bytes(data)
        # volume
        volume = Float.from_bytes(data)
        # pitch
        pitch = Float.from_bytes(data)
        # seed
        seed = Long.from_bytes(data)
        return cls(sound_id, sound_category, x, y, z, volume, pitch, seed)


class StopSound(Packet):
    """
    Sent by the server to the client to stop a sound effect.

    **Packet ID**: ``0x63``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x63
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        flags: Byte,
        source: Varint | None,
        sound: Identifier | None,
    ):
        self.flags = flags
        self.source = source
        self.sound = sound

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.flags)
            + bytes(self.source)
            + bytes(self.sound)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: flags (byte), source (varint), sound (identifier)
        # flags
        flags = Byte.from_bytes(data)
        # source
        source = Varint.from_bytes(data)
        # sound
        sound = Identifier.from_bytes(data)
        return cls(flags, source, sound)


class SystemChatMessage(Packet):
    """
    Sent by the server to the client to send a chat message.

    **Packet ID**: ``0x64``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x64
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        content: Chat,
        overlay: Boolean,
    ):
        self.content = content
        self.overlay = overlay

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.content)
            + bytes(self.overlay)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: content (chat), overlay (boolean)
        # content
        content = Chat.from_bytes(data)
        # overlay
        overlay = Boolean.from_bytes(data)
        return cls(content, overlay)


class SetTabListHeaderAndFooter(Packet):
    """
    Sent by the server to the client to set the header and footer of the tab list.

    **Packet ID**: ``0x65``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x65
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        header: Chat | None,
        footer: Chat | None,
    ):
        self.header = header
        self.footer = footer

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") + bytes(self.header) + bytes(self.footer)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: header (chat), footer (chat)
        # header
        header = Chat.from_bytes(data)
        # footer
        footer = Chat.from_bytes(data)
        return cls(header, footer)


class TagQueryResponse(Packet):
    """
    Sent in response to Query Block Entity Tag or Query Entity Tag.

    **Packet ID**: ``0x66``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x66
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        transaction_id: Varint,
        nbt: NBT,
    ):
        self.transaction_id = transaction_id
        self.nbt = nbt

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.transaction_id)
            + bytes(self.nbt)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: transaction_id (varint), nbt (nbt)
        # transaction_id
        transaction_id = Varint.from_bytes(data)
        # nbt
        nbt = NBT.from_bytes(data)
        return cls(transaction_id, nbt)


class PickupItem(Packet):
    """
    Sent by the server to the client to spawn a pickup item.

    **Packet ID**: ``0x67``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x67
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        collected_entity_id: Varint,
        collector_entity_id: Varint,
        pickup_item_count: Varint,
    ):
        self.collected_entity_id = collected_entity_id
        self.collector_entity_id = collector_entity_id
        self.pickup_item_count = pickup_item_count

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.collected_entity_id)
            + bytes(self.collector_entity_id)
            + bytes(self.pickup_item_count)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: collected_entity_id (varint), collector_entity_id (varint), pickup_item_count (varint)
        # collected_entity_id
        collected_entity_id = Varint.from_bytes(data)
        # collector_entity_id
        collector_entity_id = Varint.from_bytes(data)
        # pickup_item_count
        pickup_item_count = Varint.from_bytes(data)
        return cls(collected_entity_id, collector_entity_id, pickup_item_count)


class TeleportEntity(Packet):
    """
    Sent by the server to the client to teleport an entity.

    **Packet ID**: ``0x68``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x68
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        x: Double,
        y: Double,
        z: Double,
        yaw: Angle,
        pitch: Angle,
        on_ground: Boolean,
    ):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.yaw)
            + bytes(self.pitch)
            + bytes(self.on_ground)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), x (double), y (double), z (double), yaw (angle), pitch (angle), on_ground (boolean)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # x
        x = Double.from_bytes(data)
        # y
        y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # yaw
        yaw = Angle.from_bytes(data)
        # pitch
        pitch = Angle.from_bytes(data)
        # on_ground
        on_ground = Boolean.from_bytes(data)
        return cls(entity_id, x, y, z, yaw, pitch, on_ground)


class UpdateAdvancements(Packet):
    """
    Sent by the server to the client to update the advancements.

    **Packet ID**: ``0x69``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x69
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        reset: Boolean,
        mapping: dict[Identifier, Advancement],
        identifiers: list[Identifier],
        progress: list[AdvancementProgress],
    ):
        self.reset = reset
        self.mapping = mapping
        self.identifiers = identifiers
        self.progress = progress

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.reset)
            + bytes(Varint(len(self.mapping)))
            + b"".join(
                bytes(Identifier(key)) + bytes(value)
                for key, value in self.mapping.items()
            )
            + bytes(Varint(len(self.identifiers)))
            + b"".join(bytes(identifier) for identifier in self.identifiers)
            + bytes(Varint(len(self.progress)))
            + b"".join(bytes(progress) for progress in self.progress)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: reset (boolean), mapping (dictionary), identifiers (list), progress (list)
        # reset
        reset = Boolean.from_bytes(data)
        # mapping
        mapping = {}
        for _ in range(Varint.from_bytes(data).value):
            key = Identifier.from_bytes(data)
            value = Advancement.from_bytes(data)
            mapping[key] = value
        # identifiers
        identifiers = []
        for _ in range(Varint.from_bytes(data).value):
            identifiers.append(Identifier.from_bytes(data))
        # progress
        progress = []
        for _ in range(Varint.from_bytes(data).value):
            progress.append(AdvancementProgress.from_bytes(data))
        return cls(reset, mapping, identifiers, progress)


class UpdateAttributes(Packet):
    """
    Sets attributes on the given entity.

    **Packet ID**: ``0x6A``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x6A
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        attributes: list[_DataProxy],
    ):
        self.entity_id = entity_id
        self.attributes = attributes

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(Varint(len(self.attributes)))
            + b"".join(
                bytes(attribute.key)
                + bytes(attribute.value)
                + bytes(Varint(len(attribute.modifiers)))
                + b"".join(
                    bytes(mod.uuid) + bytes(mod.amount) + bytes(mod.operation)
                    for mod in attribute.modifiers
                )
                for attribute in self.attributes
            )
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), attributes (list)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # attributes
        attributes = []
        for _ in range(Varint.from_bytes(data).value):
            key = Identifier.from_bytes(data)
            value = Double.from_bytes(data)
            modifiers = []
            for _ in range(Varint.from_bytes(data).value):
                uuid = UUID.from_bytes(data)
                amount = Double.from_bytes(data)
                operation = Varint.from_bytes(data)
                modifiers.append(
                    _DataProxy(uuid=uuid, amount=amount, operation=operation)
                )
            attributes.append(_DataProxy(key=key, value=value, modifiers=modifiers))
        return cls(entity_id, attributes)


class FeatureFlags(Packet):
    """
    Used to enable and disable features, generally experimental ones, on the client.

    **Packet ID**: ``0x6B``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x6B
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        features: list[Identifier],
    ):
        self.features = features

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(Varint(len(self.features)))
            + b"".join(bytes(feature) for feature in self.features)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: features (list)
        # features
        features = []
        for _ in range(Varint.from_bytes(data).value):
            features.append(Identifier.from_bytes(data))
        return cls(features)


class EntityEffect(Packet):
    """
    Applies an effect to the given entity.

    **Packet ID**: ``0x6C``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x6C
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        entity_id: Varint,
        effect_id: Byte,
        amplifier: Byte,
        duration: Varint,
        flags: Byte,
        factor_codec: NBT,
    ):
        self.entity_id = entity_id
        self.effect_id = effect_id
        self.amplifier = amplifier
        self.duration = duration
        self.flags = flags
        self.factor_codec = factor_codec

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.effect_id)
            + bytes(self.amplifier)
            + bytes(self.duration)
            + bytes(self.flags)
            + bytes(Boolean(self.factor_codec is not None))
            + bytes(self.factor_codec)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), effect_id (byte), amplifier (byte), duration (varint), flags (byte),
        # factor_codec (nbt) entity_id
        entity_id = Varint.from_bytes(data)
        # effect_id
        effect_id = Byte.from_bytes(data)
        # amplifier
        amplifier = Byte.from_bytes(data)
        # duration
        duration = Varint.from_bytes(data)
        # flags
        flags = Byte.from_bytes(data)
        # factor_codec
        factor_codec = NBT.from_bytes(data) if Boolean.from_bytes(data) else None
        return cls(entity_id, effect_id, amplifier, duration, flags, factor_codec)


class UpdateRecipes(Packet):
    """
    Updates the recipes on the client.

    **Packet ID**: ``0x6D``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x6D
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        recipes: list[Recipe],
    ):
        self.recipes = recipes

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(Varint(len(self.recipes)))
            + b"".join(bytes(recipe) for recipe in self.recipes)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: recipes (list)
        # recipes
        recipes = []
        total_len = Varint.from_bytes(data).value
        for _ in range(total_len):
            recipes.append(Recipe.from_bytes(data))
        return cls(recipes)


class UpdateTags(Packet):
    """
    Updates the tags on the client.

    **Packet ID**: ``0x6E``

    **State**: :attr:`.State.PLAY`

    **Bound to**: Client
    """

    packet_id = 0x6E
    bound_to = "client"
    state = State.PLAY

    def __init__(
        self,
        tags: list[_DataProxy],
    ):
        self.tags = tags

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(Varint(len(self.tags)))
            + b"".join(
                (
                    bytes(tag.tag_name)
                    + bytes(Varint(len(tag.entries)))
                    + b"".join(bytes(entry) for entry in tag.entries)
                )
                for tag in self.tags
            )
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: tags (list)
        # tags
        tags = []
        for _ in range(Varint.from_bytes(data).value):
            tags.append(
                _DataProxy(
                    tag_name=Identifier.from_bytes(data),
                    entries=[
                        Varint.from_bytes(data)
                        for _ in range(Varint.from_bytes(data).value)
                    ],
                )
            )
        return cls(tags)
