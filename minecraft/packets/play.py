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
from .base import Packet
from ..datatypes import *
from ..enums import Animation

class SpawnEntity(Packet):
    """
    Spawn entity packet sent by the server to the client to spawn an entity.

    Packet ID: 0x00
    State: Play
    Bound to: Client
    """

    packet_id = 0x00

    def __init__(self, entity_id: Varint, entity_uuid: UUID, entity_type: Varint, x: Double, y: Double, z: Double, pitch: Angle, yaw: Angle, head_yaw: Angle, data: Varint, velocity_x: Short, velocity_y: Short, velocity_z: Short):
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
    def _from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), entity_uuid (uuid), entity_type (varint), x (double), y (double), z (double), pitch (angle), yaw (angle), head_yaw (angle), data (varint), velocity_x (short), velocity_y (short), velocity_z (short)
        # entity_id
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
        data = Varint.from_bytes(data)
        # velocity_x
        velocity_x = Short.from_bytes(data)
        # velocity_y
        velocity_y = Short.from_bytes(data)
        # velocity_z
        velocity_z = Short.from_bytes(data)
        return cls(entity_id, entity_uuid, entity_type, x, y, z, pitch, yaw, head_yaw, data, velocity_x, velocity_y, velocity_z)

    def __repr__(self):
        return (
            f"SpawnEntity({self.entity_id!r}, {self.entity_uuid!r}, {self.entity_type!r}, "
            f"{self.x!r}, {self.y!r}, {self.z!r}, {self.pitch!r}, {self.yaw!r}, {self.head_yaw!r}, "
            f"{self.data!r}, {self.velocity_x!r}, {self.velocity_y!r}, {self.velocity_z!r})"
        )


class SpawnExperienceOrb(Packet):
    """
    Spawn experience orb packet sent by the server to the client to spawn an experience orb.

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
    def _from_bytes(cls, data: BytesIO):
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
    Spawn player packet sent by the server to the client to spawn a player.

    Packet ID: 0x02
    State: Play
    Bound to: Client
    """

    packet_id = 0x02

    def __init__(self, entity_id: Varint, player_uuid: UUID, x: Double, y: Double, z: Double, yaw: Angle, pitch: Angle, current_item: Short, metadata: Metadata):
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
    def _from_bytes(cls, data: BytesIO):
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
        return f"SpawnPlayer({self.entity_id!r}, {self.player_uuid!r}, {self.x!r}, {self.y!r}, {self.z!r}, {self.yaw!r}, {self.pitch!r})"


class EntityAnimation(Packet):
    """
    Entity animation packet sent by the server to the client to animate an entity.

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
            bytes(self.animation)
        )

    @classmethod
    def _from_bytes(cls, data: BytesIO):
        # Fields: entity_id (varint), animation_id (varint)
        # entity_id
        entity_id = Varint.from_bytes(data)
        # animation
        animation_id = UnsignedByte.from_bytes(data)
        return cls(entity_id, animation_id)

    def __repr__(self):
        return f"EntityAnimation({self.entity_id!r}, {self.animation!r})"


