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
=
from .base import Packet
from ..datatypes import *
from ..enums import (
    Animation,
    BossBarColor,
    BossBarDivision,
    ChatSuggestionAction,
    FeetEyes,
    FilterType,
    GameEvents,
    Hand,
    RecipeBookActionType,
    WorldEvents,
)


class SpawnEntity(Packet):
    """
    Sent by the server when a vehicle or other non-living entity is created.

    Packet ID: 0x00
    State: Play
    Bound to: Client
    """

    packet_id = 0x00

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

    Packet ID: 0x01
    State: Play
    Bound to: Client
    """

    packet_id = 0x01

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

    Packet ID: 0x02
    State: Play
    Bound to: Client
    """

    packet_id = 0x02

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

    Packet ID: 0x03
    State: Play
    Bound to: Client
    """

    packet_id = 0x03

    def __init__(self, entity_id: Varint, animation_id: UnsignedByte):
        self.entity_id = entity_id
        self.animation_id = animation_id

    @property
    def animation(self):
        return Animation(self.animation_id)

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.animation_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), animation_id (varint)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # animation
        animation_id = UnsignedByte.from_bytes(data)
        return cls(entity_id, animation_id)


class AwardStats(Packet):
    """
    Sent as a response to Client Command (id 1).
    Will only send the changed values if previously requested.

    Packet ID: 0x04
    State: Play
    Bound to: Client
    """

    packet_id = 0x04

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

    Packet ID: 0x05
    State: Play
    Bound to: Client
    """

    packet_id = 0x05

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
    0–9 are the displayable destroy stages and each other
    number means that there is no animation on this coordinate.

    Packet ID: 0x06
    State: Play
    Bound to: Client
    """

    packet_id = 0x06

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

    Packet ID: 0x07
    State: Play
    Bound to: Client
    """

    packet_id = 0x07

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

    Packet ID: 0x08
    State: Play
    Bound to: Client
    """

    packet_id = 0x08

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

    Packet ID: 0x09
    State: Play
    Bound to: Client
    """

    packet_id = 0x09

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

    Packet ID: 0x0A
    State: Play
    Bound to: Client
    """

    packet_id = 0x0A

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
                    + bytes(self.color.value)
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
                res += bytes(self.color.value) + bytes(
                    self.division.value
                )  # type: ignore
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
                color = BossBarColor(Varint.from_bytes(data))
                division = Varint.from_bytes(data)
                flags = UnsignedByte.from_bytes(data)
            case 1:
                pass
            case 2:
                health = Float.from_bytes(data)
            case 3:
                title = Chat.from_bytes(data)
            case 4:
                color = BossBarColor(Varint.from_bytes(data))
                division = Varint.from_bytes(data)
            case 5:
                flags = UnsignedByte.from_bytes(data)
            case _:
                raise ValueError(f"Invalid action value {action.value}")
        return cls(uuid, action, title, health, color, division, flags)


class ChangeDifficulty(Packet):
    """
    Changes the difficulty setting in the client's option menu.

    Packet ID: 0x0B
    State: Play
    Bound to: Client
    """

    packet_id = 0x0B

    def __init__(self, difficulty: UnsignedByte, locked: Boolean = Boolean(False)):
        self.difficulty: UnsignedByte = difficulty
        self.locked: Boolean = locked

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.difficulty)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: difficulty (unsigned byte)
        # difficulty
        difficulty = UnsignedByte.from_bytes(data)
        locked = Boolean(False)
        if data.read(1):
            locked = Boolean.from_bytes(data)
        return cls(difficulty, locked)


class ClearTitles(Packet):
    """
    Clear the client's current title information, with the option to also reset it.

    Packet ID: 0x0C
    State: Play
    Bound to: Client
    """

    packet_id = 0x0C

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

    Packet ID: 0x0D
    State: Play
    Bound to: Client
    """

    packet_id = 0x0D

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

    Packet ID: 0x0E
    State: Play
    Bound to: Client
    """

    packet_id = 0x0E

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

    Packet ID: 0x0F
    State: Play
    Bound to: Client
    """

    packet_id = 0x0F

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

    Packet ID: 0x10
    State: Play
    Bound to: Client
    """

    packet_id = 0x10

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

    Packet ID: 0x11
    State: Play
    Bound to: Client
    """

    packet_id = 0x11

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

    Packet ID: 0x12
    State: Play
    Bound to: Client
    """

    packet_id = 0x12

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

    Packet ID: 0x13
    State: Play
    Bound to: Client
    """

    packet_id = 0x13

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

    Packet ID: 0x14
    State: Play
    Bound to: Client
    """

    packet_id = 0x14

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


class PluginMessage(Packet):
    """
    Mods and plugins can use this to send their data.
    Minecraft itself uses several plugin channels.
    These internal channels are in the minecraft namespace.

    Packet ID: 0x15
    State: Play
    Bound to: Client
    """

    packet_id = 0x15

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


class DeleteMessage(Packet):
    """
    Sent by the server to delete a message from the client's chat.

    Packet ID: 0x16
    State: Play
    Bound to: Client
    """

    packet_id = 0x16

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

    Packet ID: 0x17
    State: Play
    Bound to: Client
    """

    packet_id = 0x17

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

    Packet ID: 0x18
    State: Play
    Bound to: Client
    """

    packet_id = 0x18

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

    Packet ID: 0x19
    State: Play
    Bound to: Client
    """

    packet_id = 0x19

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

    Packet ID: 0x1A
    State: Play
    Bound to: Client
    """

    packet_id = 0x1A

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

    Packet ID: 0x1B
    State: Play
    Bound to: Client
    """

    packet_id = 0x1B

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

    Packet ID: 0x1C
    State: Play
    Bound to: Client
    """

    packet_id = 0x1C

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
        event = GameEvents(UnsignedByte.from_bytes(data))
        # value
        value = Float.from_bytes(data)
        return cls(event, value)


class OpenHorseScreen(Packet):
    """
    Opens the horse inventory screen.

    Packet ID: 0x1D
    State: Play
    Bound to: Client
    """

    packet_id = 0x1D

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


class InitializeWorldBorder(Packet):
    """
    Initializes the world border.

    Packet ID: 0x1E
    State: Play
    Bound to: Client
    """

    packet_id = 0x1E

    def __init__(
        self,
        x: Double,
        z: Double,
        old_diameter: Double,
        new_diameter: Double,
        speed: Varlong,
        portal_teleport_boundary: Varint,
        warning_blocks: Varint,
        warning_time: Varint,
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


class KeepAliveServer(Packet):
    """
    The server will frequently send out a keep-alive, each containing a random ID.
    The client must respond with the same payload (see serverbound Keep Alive).
    If the client does not respond to them for over 30 seconds,
    the server kicks the client.
    Vice versa, if the server does not send any keep-alives for 20 seconds,
    the client will disconnect and yields a "Timed out" exception.

    Packet ID: 0x1F
    State: Play
    Bound to: Client
    """

    packet_id = 0x1F

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

    Packet ID: 0x20
    State: Play
    Bound to: Client
    """

    packet_id = 0x20

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

    Packet ID: 0x21
    State: Play
    Bound to: Client
    """

    packet_id = 0x21

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
        event = WorldEvents(Int.from_bytes(data))
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

    Packet ID: 0x22
    State: Play
    Bound to: Client
    """

    packet_id = 0x22

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

    Packet ID: 0x23
    State: Play
    Bound to: Client
    """

    packet_id = 0x23

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

    Packet ID: 0x24
    State: Play
    Bound to: Client
    """

    packet_id = 0x24

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

    Packet ID: 0x25
    State: Play
    Bound to: Client
    """

    packet_id = 0x25

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

    Packet ID: 0x26
    State: Play
    Bound To: Client
    """

    packet_id = 0x26

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

    Packet ID: 0x27
    State: Play
    Bound To: Client
    """

    packet_id = 0x27

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

    Packet ID: 0x28
    State: Play
    Bound To: Client
    """

    packet_id = 0x28

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

    Packet ID: 0x29
    State: Play
    Bound To: Client
    """

    packet_id = 0x29

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

    Packet ID: 0x2A
    State: Play
    Bound To: Client
    """

    packet_id = 0x2A

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

    Packet ID: 0x2B
    State: Play
    Bound To: Client
    """

    packet_id = 0x2B

    def __init__(self, hand: Hand):
        self.hand = hand

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.hand)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: hand (hand)
        # hand
        hand = Hand.from_bytes(data)
        return cls(hand)


class OpenScreen(Packet):
    """
    This is sent to the client when it should open an inventory,
    such as a chest, workbench, furnace, or other container.

    Packet ID: 0x2C
    State: Play
    Bound To: Client
    """

    packet_id = 0x2C

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

    Packet ID: 0x2D
    State: Play
    Bound To: Client
    """

    packet_id = 0x2D

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

    Packet ID: 0x2E
    State: Play
    Bound To: Client
    """

    packet_id = 0x2E

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

    Packet ID: 0x2F
    State: Play
    Bound To: Client
    """

    packet_id = 0x2F

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


class PlayerAbilities(Packet):
    """
    This packet is sent by the server to update the client's
    abilities and flags.

    Packet ID: 0x30
    State: Play
    Bound To: Client
    """

    packet_id = 0x30

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

    Packet ID: 0x31
    State: Play
    Bound To: Server
    """

    packet_id = 0x31

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
        filter_type = FilterType(Varint.from_bytes(data))
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

    Packet ID: 0x32
    State: Play
    Bound To: Client
    """

    packet_id = 0x32

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

    Packet ID: 0x33
    State: Play
    Bound To: Client
    """

    packet_id = 0x33


class CombatDeath(Packet):
    """
    Used to send a respawn screen.

    Packet ID: 0x34
    State: Play
    Bound To: Client
    """

    packet_id = 0x34

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

    Packet ID: 0x35
    State: Play
    Bound To: Client
    """

    packet_id = 0x35

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

    Packet ID: 0x36
    State: Play
    Bound To: Client
    """

    packet_id = 0x36

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

    Packet ID: 0x37
    State: Play
    Bound To: Client
    """

    packet_id = 0x37

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
        feet_eyes = FeetEyes(Varint.from_bytes(data))
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
        entity_feet_eyes = FeetEyes(Varint.from_bytes(data)) if is_entity else None
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

    Packet ID: 0x38
    State: Play
    Bound To: Client
    """

    packet_id = 0x38

    def __init__(
        self,
        x: Double,
        y: Double,
        z: Double,
        feet_eyes: FeetEyes,
        flags: Byte,
        teleport_id: Varint,
        dismount_vehicle: Boolean,
    ):
        self.x = x
        self.y = y
        self.z = z
        self.feet_eyes = feet_eyes
        self.flags = flags
        self.teleport_id = teleport_id
        self.dismount_vehicle = dismount_vehicle

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.feet_eyes)
            + bytes(self.flags)
            + bytes(self.teleport_id)
            + bytes(self.dismount_vehicle)
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
        feet_eyes = FeetEyes(Varint.from_bytes(data))
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

    Packet ID: 0x39
    State: Play
    Bound To: Client
    """

    packet_id = 0x39

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
        action = RecipeBookActionType(Varint.from_bytes(data))
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

    Packet ID: 0x3A
    State: Play
    Bound To: Client
    """

    packet_id = 0x3A

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

    Packet ID: 0x3B
    State: Play
    Bound To: Client
    """

    packet_id = 0x3B

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

    Packet ID: 0x3C
    State: Play
    Bound To: Client
    """

    packet_id = 0x3C

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

    Packet ID: 0x3D
    State: Play
    Bound To: Client
    """

    packet_id = 0x3D

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
        death_dimension: Identifier | None,
        death_location: Position | None,
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

    Packet ID: 0x3E
    State: Play
    Bound To: Client
    """

    packet_id = 0x3E

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


class e:
    ...
