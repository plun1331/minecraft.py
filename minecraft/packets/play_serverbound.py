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

from .base import Packet
from .. import (
    BlockFace,
    ChatMode,
    ClientCommandAction,
    Hand,
    InteractionType,
    MainHand,
    PlayerActionStatus,
    PlayerCommandAction,
)
from ..datatypes import *


class ConfirmTeleportation(Packet):
    """
    Sent by client as confirmation of Synchronize Player Position.

    Packet ID: 0x00
    State: Play
    Bound to: Server
    """

    packet_id = 0x00

    def __init__(self, teleport_id: Varint):
        self.teleport_id = teleport_id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.teleport_id)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: teleport_id (Varint)
        # teleport_id
        teleport_id = Varint.from_bytes(data)
        return cls(teleport_id)


class QueryBlockEntityTag(Packet):
    """
    Used when ``Shift+F3+I`` is pressed while looking at a block.

    Packet ID: 0x01
    State: Play
    Bound to: Server
    """

    packet_id = 0x01

    def __init__(self, transaction_id: Varint, location: Position):
        self.transaction_id = transaction_id
        self.location = location

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.transaction_id)
            + bytes(self.location)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: transaction_id (Varint), location (Position)
        # transaction_id
        transaction_id = Varint.from_bytes(data)
        # location
        location = Position.from_bytes(data)
        return cls(transaction_id, location)


class ChangeDifficulty(Packet):
    """
    Only be used on singleplayer;
    the difficulty buttons are disabled in multiplayer.

    Packet ID: 0x02
    State: Play
    Bound to: Server
    """

    packet_id = 0x02

    def __init__(self, difficulty: UnsignedByte):
        self.difficulty = difficulty

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.difficulty)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: difficulty (UnsignedByte)
        # difficulty
        difficulty = UnsignedByte.from_bytes(data)
        return cls(difficulty)


class MessageAcknowledgement(Packet):
    """
    Sent by client to acknowledge a message.

    Packet ID: 0x03
    State: Play
    Bound to: Server
    """

    packet_id = 0x03

    def __init__(self, message_count: Varint):
        self.message_count = message_count

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.message_count)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: message_count (Varint)
        # message_count
        message_count = Varint.from_bytes(data)
        return cls(message_count)


class ChatCommand(Packet):
    """
    Sent by client to send a command.

    Packet ID: 0x04
    State: Play
    Bound to: Server
    """

    packet_id = 0x04

    def __init__(
        self,
        command: String,
        timestamp: Long,
        salt: Long,
        argument_signatures: list[tuple[String, ByteArray]],
        message_count: Varint,
        acknowledged: BitSet,
    ):
        self.command = command
        self.timestamp = timestamp
        self.salt = salt
        self.argument_signatures = argument_signatures
        self.message_count = message_count
        self.acknowledged = acknowledged

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.command)
            + bytes(self.timestamp)
            + bytes(self.salt)
            + bytes(Varint(len(self.argument_signatures)))
            + b"".join(
                bytes(name) + bytes(sig) for name, sig in self.argument_signatures
            )
            + bytes(self.message_count)
            + bytes(self.acknowledged)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: command (String), timestamp (Long), salt (Long),
        # argument_signatures (tuple[String, ByteArray]), message_count (Varint), acknowledged (BitSet)
        # command
        command = String.from_bytes(data)
        # timestamp
        timestamp = Long.from_bytes(data)
        # salt
        salt = Long.from_bytes(data)
        # argument_signatures
        argument_signatures = []
        for _ in range(Varint.from_bytes(data).value):
            argument_signatures.append(
                (
                    String.from_bytes(data),
                    ByteArray.from_bytes(data),
                )
            )
        # message_count
        message_count = Varint.from_bytes(data)
        # acknowledged
        acknowledged = BitSet.from_bytes(data)
        return cls(
            command,
            timestamp,
            salt,
            argument_signatures,
            message_count,
            acknowledged,
        )


class ChatMessage(Packet):
    """
    Send a chat message.

    Packet ID: 0x05
    State: Play
    Bound to: Server
    """

    packet_id = 0x05

    def __init__(
        self,
        message: String,
        timestamp: Long,
        salt: Long,
        signature: ByteArray | None,
        message_count: Varint,
        acknowledged: BitSet,
    ):
        self.message = message
        self.timestamp = timestamp
        self.salt = salt
        self.signature = signature
        self.message_count = message_count
        self.acknowledged = acknowledged

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.message)
            + bytes(self.timestamp)
            + bytes(self.salt)
            + bytes(Boolean(self.signature is not None))
            + (bytes(self.signature) if self.signature is not None else b"")
            + bytes(self.message_count)
            + bytes(self.acknowledged)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: message (String), timestamp (Long), salt (Long), signature (ByteArray),
        # message_count (Varint), acknowledged (BitSet)
        # message
        message = String.from_bytes(data)
        # timestamp
        timestamp = Long.from_bytes(data)
        # salt
        salt = Long.from_bytes(data)
        # signature
        if Boolean.from_bytes(data).value:
            signature = ByteArray.from_bytes(data)
        else:
            signature = None
        # message_count
        message_count = Varint.from_bytes(data)
        # acknowledged
        acknowledged = BitSet.from_bytes(data)
        return cls(
            message,
            timestamp,
            salt,
            signature,
            message_count,
            acknowledged,
        )


class ClientCommand(Packet):
    """
    Sent by client to send a command.

    Packet ID: 0x06
    State: Play
    Bound to: Server
    """

    packet_id = 0x06

    def __init__(
        self,
        action_id: ClientCommandAction,
    ):
        self.action_id = action_id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.action_id.value)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: action_id (ClientCommandAction)
        # action_id
        action_id = ClientCommandAction(Varint.from_bytes(data))
        return cls(action_id)


class ClientInformation(Packet):
    """
    Sent by client to send information about the client.

    Packet ID: 0x07
    State: Play
    Bound to: Server
    """

    packet_id = 0x07

    def __init__(
        self,
        locale: String,
        view_distance: Varint,
        chat_mode: ChatMode,
        chat_colors: Boolean,
        displayed_skin_parts: BitSet,
        main_hand: MainHand,
        enable_text_filtering: Boolean,
        allow_server_listings: Boolean,
    ):
        self.locale = locale
        self.view_distance = view_distance
        self.chat_mode = chat_mode
        self.chat_colors = chat_colors
        self.displayed_skin_parts = displayed_skin_parts
        self.main_hand = main_hand
        self.enable_text_filtering = enable_text_filtering
        self.allow_server_listings = allow_server_listings

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.locale)
            + bytes(self.view_distance)
            + bytes(self.chat_mode.value)
            + bytes(self.chat_colors)
            + bytes(self.displayed_skin_parts)
            + bytes(self.main_hand.value)
            + bytes(self.enable_text_filtering)
            + bytes(self.allow_server_listings)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: locale (String), view_distance (Varint), chat_mode (ChatMode),
        # chat_colors (Boolean), displayed_skin_parts (BitSet), main_hand (MainHand),
        # enable_text_filtering (Boolean), allow_server_listings (Boolean)
        # locale
        locale = String.from_bytes(data)
        # view_distance
        view_distance = Varint.from_bytes(data)
        # chat_mode
        chat_mode = ChatMode(Varint.from_bytes(data))
        # chat_colors
        chat_colors = Boolean.from_bytes(data)
        # displayed_skin_parts
        displayed_skin_parts = BitSet.from_bytes(data)
        # main_hand
        main_hand = MainHand(Varint.from_bytes(data))
        # enable_text_filtering
        enable_text_filtering = Boolean.from_bytes(data)
        # allow_server_listings
        allow_server_listings = Boolean.from_bytes(data)
        return cls(
            locale,
            view_distance,
            chat_mode,
            chat_colors,
            displayed_skin_parts,
            main_hand,
            enable_text_filtering,
            allow_server_listings,
        )


class CommandSuggestionsRequest(Packet):
    """
    Sent when the client needs to tab-complete a minecraft:ask_server suggestion type.

    Packet ID: 0x08
    State: Play
    Bound to: Server
    """

    packet_id = 0x08

    def __init__(
        self,
        transaction_id: Varint,
        text: String,
    ):
        self.transaction_id = transaction_id
        self.text = text

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.transaction_id)
            + bytes(self.text)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: transaction_id (Varint), text (String)
        # transaction_id
        transaction_id = Varint.from_bytes(data)
        # text
        text = String.from_bytes(data, max_length=32500)
        return cls(transaction_id, text)


class ClickContainerButton(Packet):
    """
    Used when clicking on window buttons.

    Packet ID: 0x09
    State: Play
    Bound to: Server
    """

    packet_id = 0x09

    def __init__(
        self,
        window_id: Byte,
        button_id: Byte,
    ):
        self.window_id = window_id
        self.button_id = button_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(self.button_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (Byte), button_id (Byte)
        # window_id
        window_id = Byte.from_bytes(data)
        # button_id
        button_id = Byte.from_bytes(data)
        return cls(window_id, button_id)


class ClickContainer(Packet):
    """
    Sent by the client when the player clicks on a slot in a window.

    Packet ID: 0x0A
    State: Play
    Bound to: Server
    """

    packet_id = 0x0A

    def __init__(
        self,
        window_id: Byte,
        state_id: Varint,
        slot: Short,
        button: Byte,
        mode: Varint,
        slots: list[tuple[Short, Slot]],
        carried_item: Slot,
    ):
        self.window_id = window_id
        self.state_id = state_id
        self.slot = slot
        self.button = button
        self.mode = mode
        self.slots = slots
        self.carried_item = carried_item

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(self.state_id)
            + bytes(self.slot)
            + bytes(self.button)
            + bytes(self.mode)
            + bytes(Varint(len(self.slots)))
            + b"".join(bytes(slot) + bytes(item) for slot, item in self.slots)
            + bytes(self.carried_item)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (Byte), state_id (Varint), slot (Short), button (Byte),
        # mode (Varint), slots (List[Short, Slot]), carried_item (Slot)
        # window_id
        window_id = Byte.from_bytes(data)
        # state_id
        state_id = Varint.from_bytes(data)
        # slot
        slot = Short.from_bytes(data)
        # button
        button = Byte.from_bytes(data)
        # mode
        mode = Varint.from_bytes(data)
        # slots
        slots = []
        for _ in range(Varint.from_bytes(data).value):
            slot = Short.from_bytes(data)
            item = Slot.from_bytes(data)
            slots.append((slot, item))
        # carried_item
        carried_item = Slot.from_bytes(data)
        return cls(
            window_id,
            state_id,
            slot,
            button,
            mode,
            slots,
            carried_item,
        )


class CloseContainer(Packet):
    """
    Sent by the client when the player closes a window.

    Packet ID: 0x0B
    State: Play
    Bound to: Server
    """

    packet_id = 0x0B

    def __init__(
        self,
        window_id: Byte,
    ):
        self.window_id = window_id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.window_id)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (Byte)
        # window_id
        window_id = Byte.from_bytes(data)
        return cls(window_id)


class PluginMessageServerbound(Packet):
    """
    Sent by the client when it wants to send a plugin message to the server.

    Packet ID: 0x0C
    State: Play
    Bound to: Server
    """

    packet_id = 0x0C

    def __init__(
        self,
        channel: Identifier,
        data: ByteArray,
    ):
        self.channel = channel
        self.data = data

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big") + bytes(self.channel) + bytes(self.data)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: channel (Identifier), data (ByteArray)
        # channel
        channel = Identifier.from_bytes(data)
        # data
        data = ByteArray.from_bytes(data)
        return cls(channel, data)


class EditBook(Packet):
    """
    Sent by the client when the player edits a book.

    Packet ID: 0x0D
    State: Play
    Bound to: Server
    """

    packet_id = 0x0D

    def __init__(
        self,
        slot: Varint,
        entries: list[String],
        title: String,
    ):
        self.slot = slot
        self.entries = entries
        self.title = title

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.slot)
            + bytes(Varint(len(self.entries)))
            + b"".join(bytes(entry) for entry in self.entries)
            + bytes(self.title)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: slot (Varint), entries (List[String]), title (String)
        # slot
        slot = Varint.from_bytes(data)
        # entries
        entries = []
        for _ in range(Varint.from_bytes(data).value):
            entries.append(String.from_bytes(data))
        # title
        title = String.from_bytes(data)
        return cls(slot, entries, title)


class QueryEntityTag(Packet):
    """
    Sent by the client when the player queries an entity's tags.

    Packet ID: 0x0E
    State: Play
    Bound to: Server
    """

    packet_id = 0x0E

    def __init__(
        self,
        transaction_id: Varint,
        entity_id: Varint,
    ):
        self.transaction_id = transaction_id
        self.entity_id = entity_id

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.transaction_id)
            + bytes(self.entity_id)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: transaction_id (Varint), entity_id (Varint)
        # transaction_id
        transaction_id = Varint.from_bytes(data)
        # entity_id
        entity_id = Varint.from_bytes(data)
        return cls(transaction_id, entity_id)


class Interact(Packet):
    """
    Sent by the client when the player interacts with an entity.

    Packet ID: 0x0F
    State: Play
    Bound to: Server
    """

    packet_id = 0x0F

    def __init__(
        self,
        entity_id: Varint,
        type: InteractionType,
        target_x: Float | None,
        target_y: Float | None,
        target_z: Float | None,
        hand: Hand | None,
        sneaking: Boolean,
    ):
        self.entity_id = entity_id
        self.type = type
        self.target_x = target_x
        self.target_y = target_y
        self.target_z = target_z
        self.hand = hand
        self.sneaking = sneaking

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.type)
            + (bytes(self.target_x) if self.target_x is not None else b"")
            + (bytes(self.target_y) if self.target_y is not None else b"")
            + (bytes(self.target_z) if self.target_z is not None else b"")
            + (bytes(self.hand) if self.hand is not None else b"")
            + bytes(self.sneaking)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (Varint), type (InteractionType), target_x (Float),
        # target_y (Float), target_z (Float), hand (Hand), sneaking (Boolean)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # type
        type = InteractionType.from_bytes(data)
        # target_x
        target_x = Float.from_bytes(data)
        # target_y
        target_y = Float.from_bytes(data)
        # target_z
        target_z = Float.from_bytes(data)
        # hand
        hand = Hand.from_bytes(data)
        # sneaking
        sneaking = Boolean.from_bytes(data)
        return cls(
            entity_id,
            type,
            target_x,
            target_y,
            target_z,
            hand,
            sneaking,
        )


class JigsawGenerate(Packet):
    """
    Sent by the client when the player generates a jigsaw structure.

    Packet ID: 0x10
    State: Play
    Bound to: Server
    """

    packet_id = 0x10

    def __init__(
        self,
        location: Position,
        levels: Varint,
        keep_jigsaws: Boolean,
    ):
        self.location = location
        self.levels = levels
        self.keep_jigsaws = keep_jigsaws

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.location)
            + bytes(self.levels)
            + bytes(self.keep_jigsaws)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: location (Position), levels (Varint), keep_jigsaws (Boolean)
        # location
        location = Position.from_bytes(data)
        # levels
        levels = Varint.from_bytes(data)
        # keep_jigsaws
        keep_jigsaws = Boolean.from_bytes(data)
        return cls(location, levels, keep_jigsaws)


class KeepAliveServerbound(Packet):
    """
    Sent by the client to keep the connection alive.

    Packet ID: 0x11
    State: Play
    Bound to: Server
    """

    packet_id = 0x11

    def __init__(
        self,
        id: Long,
    ):
        self.id = id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.id)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: id (long)
        # id
        id = Long.from_bytes(data)
        return cls(id)


class LockDifficulty(Packet):
    """
    Sent by the client when the player locks the difficulty.

    Packet ID: 0x12
    State: Play
    Bound to: Server
    """

    packet_id = 0x12

    def __init__(
        self,
        locked: Boolean,
    ):
        self.locked = locked

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.locked)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: locked (Boolean)
        # locked
        locked = Boolean.from_bytes(data)
        return cls(locked)


class SetPlayerPosition(Packet):
    """
    Updates the player's XYZ position on the server.

    Packet ID: 0x13
    State: Play
    Bound to: Server
    """

    packet_id = 0x13

    def __init__(
        self,
        x: Double,
        feet_y: Double,
        z: Double,
        on_ground: Boolean,
    ):
        self.x = x
        self.feet_y = feet_y
        self.z = z
        self.on_ground = on_ground

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.x)
            + bytes(self.feet_y)
            + bytes(self.z)
            + bytes(self.on_ground)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: x (Double), feet_y (Double), z (Double), on_ground (Boolean)
        # x
        x = Double.from_bytes(data)
        # feet_y
        feet_y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # on_ground
        on_ground = Boolean.from_bytes(data)
        return cls(x, feet_y, z, on_ground)


class SetPlayerPositionAndRotation(Packet):
    """
    Sent by the client when the player moves and rotates.

    Packet ID: 0x14
    State: Play
    Bound to: Server
    """

    packet_id = 0x14

    def __init__(
        self,
        x: Double,
        feet_y: Double,
        z: Double,
        yaw: Float,
        pitch: Float,
        on_ground: Boolean,
    ):
        self.x = x
        self.feet_y = feet_y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.x)
            + bytes(self.feet_y)
            + bytes(self.z)
            + bytes(self.yaw)
            + bytes(self.pitch)
            + bytes(self.on_ground)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: x (Double), feet_y (Double), z (Double), yaw (Float), pitch (Float), on_ground (Boolean)
        # x
        x = Double.from_bytes(data)
        # feet_y
        feet_y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # yaw
        yaw = Float.from_bytes(data)
        # pitch
        pitch = Float.from_bytes(data)
        # on_ground
        on_ground = Boolean.from_bytes(data)
        return cls(x, feet_y, z, yaw, pitch, on_ground)


class SetPlayerRotation(Packet):
    """
    Sent by the client when the player rotates.

    Packet ID: 0x15
    State: Play
    Bound to: Server
    """

    packet_id = 0x15

    def __init__(
        self,
        yaw: Float,
        pitch: Float,
        on_ground: Boolean,
    ):
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.yaw)
            + bytes(self.pitch)
            + bytes(self.on_ground)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: yaw (Float), pitch (Float), on_ground (Boolean)
        # yaw
        yaw = Float.from_bytes(data)
        # pitch
        pitch = Float.from_bytes(data)
        # on_ground
        on_ground = Boolean.from_bytes(data)
        return cls(yaw, pitch, on_ground)


class SetPlayerOnGround(Packet):
    """
    Sent by the client when the player moves on the ground.

    Packet ID: 0x16
    State: Play
    Bound to: Server
    """

    packet_id = 0x16

    def __init__(
        self,
        on_ground: Boolean,
    ):
        self.on_ground = on_ground

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.on_ground)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: on_ground (Boolean)
        # on_ground
        on_ground = Boolean.from_bytes(data)
        return cls(on_ground)


class MoveVehicle(Packet):
    """
    Sent by the client when the player moves the vehicle.

    Packet ID: 0x17
    State: Play
    Bound to: Server
    """

    packet_id = 0x17

    def __init__(
        self,
        x: Double,
        y: Double,
        z: Double,
        yaw: Float,
        pitch: Float,
    ):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.x)
            + bytes(self.y)
            + bytes(self.z)
            + bytes(self.yaw)
            + bytes(self.pitch)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: x (Double), y (Double), z (Double), yaw (Float), pitch (Float)
        # x
        x = Double.from_bytes(data)
        # y
        y = Double.from_bytes(data)
        # z
        z = Double.from_bytes(data)
        # yaw
        yaw = Float.from_bytes(data)
        # pitch
        pitch = Float.from_bytes(data)
        return cls(x, y, z, yaw, pitch)


class PaddleBoat(Packet):
    """
    Sent by the client when the player paddles the boat.

    Packet ID: 0x18
    State: Play
    Bound to: Server
    """

    packet_id = 0x18

    def __init__(
        self,
        left_paddle_turning: Boolean,
        right_paddle_turning: Boolean,
    ):
        self.left_paddle_turning = left_paddle_turning
        self.right_paddle_turning = right_paddle_turning

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.left_paddle_turning)
            + bytes(self.right_paddle_turning)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: left_paddle_turning (Boolean), right_paddle_turning (Boolean)
        # left_paddle_turning
        left_paddle_turning = Boolean.from_bytes(data)
        # right_paddle_turning
        right_paddle_turning = Boolean.from_bytes(data)
        return cls(left_paddle_turning, right_paddle_turning)


class PickItem(Packet):
    """
    Sent by the client when the player picks an item.

    Packet ID: 0x19
    State: Play
    Bound to: Server
    """

    packet_id = 0x19

    def __init__(
        self,
        slot: Varint,
    ):
        self.slot = slot

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.slot)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: slot (Varint)
        # slot
        slot = Varint.from_bytes(data)
        return cls(slot)


class PlaceRecipe(Packet):
    """
    Sent by the client when the player places a recipe.

    Packet ID: 0x1A
    State: Play
    Bound to: Server
    """

    packet_id = 0x1A

    def __init__(
        self,
        window_id: Byte,
        recipe: Identifier,
        make_all: Boolean,
    ):
        self.window_id = window_id
        self.recipe = recipe
        self.make_all = make_all

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.window_id)
            + bytes(self.recipe)
            + bytes(self.make_all)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: window_id (Byte), recipe (Identifier), make_all (Boolean)
        # window_id
        window_id = Byte.from_bytes(data)
        # recipe
        recipe = Identifier.from_bytes(data)
        # make_all
        make_all = Boolean.from_bytes(data)
        return cls(window_id, recipe, make_all)


class PlayerAbilities(Packet):
    """
    The vanilla client sends this packet when the
    player starts/stops flying with the Flags parameter changed accordingly.

    Packet ID: 0x1B
    State: Play
    Bound to: Server
    """

    packet_id = 0x1B

    def __init__(
        self,
        flags: Byte,
    ):
        self.flags = flags

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.flags)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: flags (Byte)
        # flags
        flags = Byte.from_bytes(data)
        return cls(flags)


class PlayerAction(Packet):
    """
    Sent by the client when the player performs an action.

    Packet ID: 0x1C
    State: Play
    Bound to: Server
    """

    packet_id = 0x1C

    def __init__(
        self,
        status: PlayerActionStatus,
        location: Position,
        face: BlockFace,
        sequence: Varint,
    ):
        self.status = status
        self.location = location
        self.face = face
        self.sequence = sequence

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.status.value)
            + bytes(self.location)
            + bytes(self.face.value)
            + bytes(self.sequence)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: status (Varint), location (Position), face (Varint), sequence (Varint)
        # status
        status = PlayerActionStatus(Varint.from_bytes(data))
        # location
        location = Position.from_bytes(data)
        # face
        face = BlockFace(Varint.from_bytes(data))
        # sequence
        sequence = Varint.from_bytes(data)
        return cls(status, location, face, sequence)


class PlayerCommand(Packet):
    """
    Sent by the client when the player uses a command.

    Packet ID: 0x1D
    State: Play
    Bound to: Server
    """

    packet_id = 0x1D

    def __init__(
        self,
        entity_id: Varint,
        action_id: PlayerCommandAction,
        jump_boost: Varint,
    ):
        self.entity_id = entity_id
        self.action_id = action_id
        self.jump_boost = jump_boost

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.entity_id)
            + bytes(self.action_id.value)
            + bytes(self.jump_boost)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: entity_id (Varint), action_id (Varint), jump_boost (Varint)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # action_id
        action_id = PlayerCommandAction(Varint.from_bytes(data))
        # jump_boost
        jump_boost = Varint.from_bytes(data)
        return cls(entity_id, action_id, jump_boost)


class PlayerInput(Packet):
    """
    Also known as 'Input' packet.

    Packet ID: 0x1E
    State: Play
    Bound to: Server
    """

    packet_id = 0x1E

    def __init__(
        self,
        sideways: Float,
        forward: Float,
        flags: UnsignedByte,
    ):
        self.sideways = sideways
        self.forward = forward
        self.flags = flags

    def __bytes__(self):
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.sideways)
            + bytes(self.forward)
            + bytes(self.flags)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: sideway (Float), forward (Float), flags (Byte)
        # sideway
        sideways = Float.from_bytes(data)
        # forward
        forward = Float.from_bytes(data)
        # flags
        flags = UnsignedByte.from_bytes(data)
        return cls(sideways, forward, flags)


class Pong(Packet):
    """
    Response to the clientbound packet (Ping) with the same id.

    Packet ID: 0x1F
    State: Status
    Bound to: Server
    """

    packet_id = 0x1F

    def __init__(
        self,
        id: Int,
    ):
        self.id = id

    def __bytes__(self):
        return self.packet_id.to_bytes(1, "big") + bytes(self.id)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: id (Int)
        # id
        id = Int.from_bytes(data)
        return cls(id)
