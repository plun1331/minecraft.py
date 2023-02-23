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
from .base import Packet
from ..datatypes import *
from ..enums import Animation, BossBarColor, BossBarDivision, ChatSuggestionAction


class SpawnEntity(Packet):
    """
    Sent by the server when a vehicle or other non-living entity is created.

    Packet ID: 0x00
    State: Play
    Bound to: Client
    """

    packet_id = 0x00

    def __init__(
        self, entity_id: Varint, entity_uuid: UUID, entity_type: Varint, x: Double, y: Double, z: Double, pitch: Angle,
        yaw: Angle, head_yaw: Angle, data: Varint, velocity_x: Short, velocity_y: Short, velocity_z: Short
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
                self.packet_id.to_bytes(1, "big") +
                bytes(self.entity_id) +
                bytes(self.entity_uuid) +
                bytes(self.entity_type) +
                bytes(self.x) +
                bytes(self.y) +
                bytes(self.z) +
                bytes(self.pitch) +
                bytes(self.yaw) +
                bytes(self.head_yaw) +
                bytes(self.data) +
                bytes(self.velocity_x) +
                bytes(self.velocity_y) +
                bytes(self.velocity_z)
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
            entity_id, entity_uuid, entity_type, x, y, z, pitch, yaw, head_yaw,
            _data, velocity_x, velocity_y, velocity_z
        )

    def __repr__(self):
        return (
            f"SpawnEntity({self.entity_id!r}, {self.entity_uuid!r}, {self.entity_type!r}, "
            f"{self.x!r}, {self.y!r}, {self.z!r}, {self.pitch!r}, {self.yaw!r}, {self.head_yaw!r}, "
            f"{self.data!r}, {self.velocity_x!r}, {self.velocity_y!r}, {self.velocity_z!r})"
        )


class SpawnExperienceOrb(Packet):
    """
    Spawns one or more experience orbs.

    Packet ID: 0x01
    State: Play
    Bound to: Client
    """

    packet_id = 0x01

    def __init__(self, entity_id: Varint, x: Double, y: Double, z: Double, count: Short):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.z = z
        self.count = count

    def __bytes__(self):
        return (
                self.packet_id.to_bytes(1, "big") +
                bytes(self.entity_id) +
                bytes(self.x) +
                bytes(self.y) +
                bytes(self.z) +
                bytes(self.count)
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

    def __repr__(self):
        return f"SpawnExperienceOrb({self.entity_id!r}, {self.x!r}, {self.y!r}, {self.z!r}, {self.count!r})"


class SpawnPlayer(Packet):
    """
    This packet is sent by the server when a player comes into visible range, **not** when a player joins.

    Packet ID: 0x02
    State: Play
    Bound to: Client
    """

    packet_id = 0x02

    def __init__(self, entity_id: Varint, player_uuid: UUID, x: Double, y: Double, z: Double, yaw: Angle, pitch: Angle):
        self.entity_id = entity_id
        self.player_uuid = player_uuid
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch

    def __bytes__(self):
        return (
                self.packet_id.to_bytes(1, "big") +
                bytes(self.entity_id) +
                bytes(self.player_uuid) +
                bytes(self.x) +
                bytes(self.y) +
                bytes(self.z) +
                bytes(self.yaw) +
                bytes(self.pitch)
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

    def __repr__(self):
        return f"SpawnPlayer({self.entity_id!r}, {self.player_uuid!r}, " \
               f"{self.x!r}, {self.y!r}, {self.z!r}, {self.yaw!r}, {self.pitch!r})"


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
                self.packet_id.to_bytes(1, "big") +
                bytes(self.entity_id) +
                bytes(self.animation_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), animation_id (varint)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # animation
        animation_id = UnsignedByte.from_bytes(data)
        return cls(entity_id, animation_id)

    def __repr__(self):
        return f"EntityAnimation({self.entity_id!r}, {self.animation!r})"


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

    def __repr__(self):
        return f"AwardStats({self.stats!r})"


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
        return (
                self.packet_id.to_bytes(1, "big") +
                bytes(self.sequence_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: sequence_id (varint)
        # sequence_id
        sequence_id = Varint.from_bytes(data)
        return cls(sequence_id)

    def __repr__(self):
        return f"AcknowledgeBlockChanges({self.sequence_id!r})"


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
            self.packet_id.to_bytes(1, "big") +
            bytes(self.entity_id) +
            bytes(self.location) +
            bytes(self.destroy_stage)
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

    def __repr__(self):
        return f"SetBlockDestroyStage({self.entity_id!r}, {self.location!r}, {self.destroy_stage!r})"


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
            self.packet_id.to_bytes(1, "big") +
            bytes(self.location) +
            bytes(self.type) +
            bytes(self.nbt_data)
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

    def __repr__(self):
        return f"BlockEntityData({self.location!r}, {self.type!r}, {self.nbt_data!r})"


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

    def __init__(self, location: Position, action_id: UnsignedByte, action_param: UnsignedByte, block_type: Varint):
        self.location: Position = location
        self.action_id: UnsignedByte = action_id
        self.action_param: UnsignedByte = action_param
        self.block_type: Varint = block_type

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.location) +
            bytes(self.action_id) +
            bytes(self.action_param) +
            bytes(self.block_type)
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

    def __repr__(self):
        return f"BlockAction({self.location!r}, {self.action_id!r}, {self.action_param!r}, {self.block_type!r})"


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
            self.packet_id.to_bytes(1, "big") +
            bytes(self.location) +
            bytes(self.block_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: location (position), block_id (varint)
        # location
        location = Position.from_bytes(data)
        # block_id
        block_id = Varint.from_bytes(data)
        return cls(location, block_id)

    def __repr__(self):
        return f"BlockUpdate({self.location!r}, {self.block_id!r})"


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
        res = (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.uuid) +
            bytes(self.action)
        )
        match self.action.value:
            case 0:
                res += (
                        bytes(self.title) +
                        bytes(self.health) +
                        bytes(self.color.value) +  # type: ignore
                        bytes(self.division.value) +  # type: ignore
                        bytes(self.flags)
                )
            case 1:
                pass
            case 2:
                res += bytes(self.health)
            case 3:
                res += bytes(self.title)
            case 4:
                res += bytes(self.color.value) + bytes(self.division.value)  # type: ignore
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

    def __repr__(self):
        return f"BossBar({self.uuid!r}, {self.action!r}, {self.title!r}, " \
               f"{self.health!r}, {self.color!r}, {self.division!r}, {self.flags!r})"


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
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.difficulty)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: difficulty (unsigned byte)
        # difficulty
        difficulty = UnsignedByte.from_bytes(data)
        locked = Boolean(False)
        if data.read(1):
            locked = Boolean.from_bytes(data)
        return cls(difficulty, locked)

    def __repr__(self):
        return f"ChangeDifficulty({self.difficulty!r}, {self.locked!r})"


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
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.reset)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: reset (boolean)
        # reset
        reset = Boolean.from_bytes(data)
        return cls(reset)

    def __repr__(self):
        return f"ClearTitles({self.reset!r})"


class CommandSuggestionsResponse(Packet):
    """
    The server responds with a list of auto-completions of the last word sent to it.

    Packet ID: 0x0D
    State: Play
    Bound to: Client
    """

    packet_id = 0x0D

    def __init__(self, transaction_id: Varint, start: Varint, length: Varint, matches: list[CommandSuggestionMatch]):
        self.transaction_id: Varint = transaction_id
        self.start: Varint = start
        self.length: Varint = length
        self.matches: list[CommandSuggestionMatch] = matches

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.transaction_id) +
            bytes(Varint(len(self.matches))) +
            b"".join(bytes(match) for match in self.matches)
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

    def __repr__(self):
        return f"CommandSuggestionsResponse({self.transaction_id!r}, {self.start!r}, {self.length!r}, {self.matches!r})"


class Commands(Packet):
    """
    Lists all of the commands on the server, and how they are parsed.

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
            self.packet_id.to_bytes(1, "big") +
            bytes(Varint(len(self.nodes))) +
            b"".join(bytes(node) for node in self.nodes) +
            bytes(self.root_index)
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

    def __repr__(self):
        return f"Commands({self.nodes!r}, {self.root_index!r})"


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
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.window_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (unsigned byte)
        # window_id
        window_id = UnsignedByte.from_bytes(data)
        return cls(window_id)

    def __repr__(self):
        return f"CloseContainer({self.window_id!r})"


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

    def __init__(self, window_id: UnsignedByte, state_id: Varint, contents: list[Slot], carried_item: Slot):
        self.window_id: UnsignedByte = window_id
        self.state_id: Varint = state_id
        self.contents: list[Slot] = contents
        self.carried_item: Slot = carried_item

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.window_id) +
            bytes(self.state_id) +
            bytes(Varint(len(self.contents))) +
            b"".join(bytes(slot) for slot in self.contents) +
            bytes(self.carried_item)
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

    def __repr__(self):
        return f"SetContainerContents({self.window_id!r}, {self.state_id!r}, {self.contents!r}, {self.carried_item!r})"


class SetContainerProperty(Packet):
    """
    This packet is used to inform the client that part of a GUI window should be updated.

    Packet ID: 0x11
    State: Play
    Bound to: Client
    """

    packet_id = 0x11
    # TODO:
    #  I'm unsure how to actually determine the window type,
    #  so I'll leave adding the enums for later.

    def __init__(self, window_id: UnsignedByte, property: Short, value: Short):
        self.window_id: UnsignedByte = window_id
        self.property: Short = property
        self.value: Short = value

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.window_id) +
            bytes(self.property) +
            bytes(self.value)
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

    def __repr__(self):
        return f"SetContainerProperty({self.window_id!r}, {self.property!r}, {self.value!r})"


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
            self.packet_id.to_bytes(1, "big") +
            bytes(self.window_id) +
            bytes(self.state_id) +
            bytes(self.slot) +
            bytes(self.item)
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

    def __repr__(self):
        return f"SetContainerSlot({self.window_id!r}, {self.slot!r}, {self.state_id!r}, {self.item!r})"


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
            self.packet_id.to_bytes(1, "big") +
            bytes(self.item_id) +
            bytes(self.cooldown)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: item_id (varint), cooldown (varint)
        # item_id
        item_id = Varint.from_bytes(data)
        # cooldown
        cooldown = Varint.from_bytes(data)
        return cls(item_id, cooldown)

    def __repr__(self):
        return f"SetCooldown({self.item_id!r}, {self.cooldown!r})"


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
            self.packet_id.to_bytes(1, "big") +
            bytes(self.action.value) +  # type: ignore
            bytes(Varint(len(self.entries))) +
            b"".join(bytes(entry) for entry in self.entries)
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

    def __repr__(self):
        return f"ChatSuggestions({self.action!r}, {self.entries!r})"


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
            self.packet_id.to_bytes(1, "big") +
            bytes(self.channel) +
            bytes(self.data)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: channel (identifier), data (byte array)
        # channel
        channel = Identifier.from_bytes(data)
        # data
        data = ByteArray.from_bytes(data)
        return cls(channel, data)

    def __repr__(self):
        return f"PluginMessage({self.channel!r}, {self.data!r})"


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
            self.packet_id.to_bytes(1, "big") +
            len(self.signature).to_bytes(1, "big") +
            bytes(self.signature)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: signature (byte array)
        # signature
        length = Varint.from_bytes(data).value
        signature = ByteArray.from_bytes(data, length=length)
        return cls(signature)

    def __repr__(self):
        return f"DeleteMessage({self.signature!r})"


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
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.reason)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: reason (chat)
        # reason
        reason = Chat.from_bytes(data)
        return cls(reason)

    def __repr__(self):
        return f"DisconnectPlay({self.reason!r})"


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
        return (
            self.packet_id.to_bytes(1, "big") +
            bytes(self.message)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: message (string)
        # message
        message = String.from_bytes(data)
        return cls(message)

    def __repr__(self):
        return f"DisguisedChatMessage({self.message!r})"


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
            self.packet_id.to_bytes(1, "big") +
            bytes(self.entity_id) +
            bytes(self.entity_status.value)  # type: ignore
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), entity_status (byte)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # entity_status
        entity_status = Byte.from_bytes(data)
        return cls(entity_id, entity_status)

    def __repr__(self):
        return f"EntityEvent({self.entity_id!r}, {self.entity_status!r})"


class Explosion(Packet):
    """
    Sent when an explosion occurs (creepers, TNT, and ghast fireballs).

    Packet ID: 0x1A
    State: Play
    Bound to: Client
    """

    packet_id = 0x1A

    def __init__(
        self, x: Double, y: Double, z: Double,
        strength: Float, records: list[tuple[Byte, Byte, Byte]],
        player_motion_x: Float, player_motion_y: Float, player_motion_z: Float
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
            self.packet_id.to_bytes(1, "big") +
            bytes(self.x) +
            bytes(self.y) +
            bytes(self.z) +
            bytes(self.strength) +
            len(self.records).to_bytes(1, "big") +
            b"".join(b"".join(bytes(block) for block in record) for record in self.records) +
            bytes(self.player_motion_x) +
            bytes(self.player_motion_y) +
            bytes(self.player_motion_z)
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
            records.append((
                Byte.from_bytes(data),
                Byte.from_bytes(data),
                Byte.from_bytes(data)
            ))
        # player_motion_x
        player_motion_x = Float.from_bytes(data)
        # player_motion_y
        player_motion_y = Float.from_bytes(data)
        # player_motion_z
        player_motion_z = Float.from_bytes(data)
        return cls(
            x, y, z, strength, records,
            player_motion_x, player_motion_y, player_motion_z
        )


    def __repr__(self):
        return (
            f"Explosion({self.x!r}, {self.y!r}, {self.z!r}, {self.strength!r}, "
            f"{self.records!r}, {self.player_motion_x!r}, {self.player_motion_y!r}, "
            f"{self.player_motion_z!r})"
        )
