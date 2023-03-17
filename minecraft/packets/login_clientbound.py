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
from ..datatypes import *


class DisconnectLogin(Packet):
    """
    Sent by the server when the client is disconnected.

    Packet ID: 0x00
    State: Login
    Bound To: Client
    """

    id = 0x00

    def __init__(self, reason: String) -> None:
        self.reason: String = reason

    def __bytes__(self) -> bytes:
        return bytes(self.id) + bytes(self.reason)

    @classmethod
    def from_bytes(cls, data: BytesIO):
        # Fields: reason (string)
        return cls(String.from_bytes(data))

    def __str__(self) -> str:
        return str(self.reason)


class EncryptionRequest(Packet):
    """
    Sent by the server to request encryption.

    Packet ID: 0x01
    State: Login
    Bound To: Client
    """

    packet_id = 0x01

    def __init__(
        self, server_id: String, public_key: ByteArray, verify_token: ByteArray
    ) -> None:
        self.server_id = server_id
        self.public_key = public_key
        self.verify_token = verify_token

    def __bytes__(self):
        public_key_length = Varint(len(self.public_key))
        verify_token_length = Varint(len(self.verify_token))
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.server_id)
            + bytes(public_key_length)
            + bytes(self.public_key)
            + bytes(verify_token_length)
            + bytes(self.verify_token)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "EncryptionRequest":
        # Fields: server_id (string), public key length (varint),
        # public_key (byte array), verify token length (varing), verify_token (byte array)
        # server id
        server_id = String.from_bytes(data)
        # public key length
        public_key_length = Varint.from_bytes(data).value
        # public key
        public_key = ByteArray.from_bytes(data, length=public_key_length)
        # verify token length
        verify_token_length = Varint.from_bytes(data).value
        # verify token
        verify_token = ByteArray.from_bytes(data, length=verify_token_length)
        return cls(server_id, public_key, verify_token)


class LoginSuccess(Packet):
    """
    Sent by the server to indicate that the client has successfully logged in.

    Packet ID: 0x02
    State: Login
    Bound To: Client
    """

    id = 0x02

    def __init__(
        self, uuid: UUID, username: String, properties: list[Property]
    ) -> None:
        self.uuid = uuid
        self.username = username
        self.properties = properties

    def __bytes__(self) -> bytes:
        return bytes(self.id) + bytes(self.uuid) + bytes(self.username)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "LoginSuccess":
        # Fields: uuid (string), username (string), property count (varint), properties (array of property)
        # uuid
        uuid = UUID.from_bytes(data)
        # username
        username = String.from_bytes(data)
        # property count
        property_count = Varint.from_bytes(data).value
        # properties
        properties = []
        for _ in range(property_count):
            properties.append(Property.from_bytes(data))
        return cls(uuid, username, properties)


class SetCompression(Packet):
    """
    Sent by the server to indicate that the client should use compression.

    Packet ID: 0x03
    State: Login
    Bound To: Client
    """

    id = 0x03

    def __init__(self, threshold: Varint) -> None:
        self.threshold = threshold

    def __bytes__(self) -> bytes:
        return bytes(self.id) + bytes(self.threshold)

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "SetCompression":
        # Fields: threshold (varint)
        # threshold
        threshold = Varint.from_bytes(data)
        return cls(threshold)


class LoginPluginRequest(Packet):
    """
    Used to implement a custom handshaking flow together with Login Plugin Response.
    Our client should always respond that it hasn't understood the request.

    Packet ID: 0x04
    State: Login
    Bound To: Client
    """

    packet_id = 0x04

    def __init__(self, message_id: Varint, channel: String, data: ByteArray) -> None:
        self.message_id = message_id
        self.channel = channel
        self.data = data

    def __bytes__(self) -> bytes:
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.message_id)
            + bytes(self.channel)
            + bytes(self.data)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "LoginPluginRequest":
        # Fields: message id (varint), channel (string), data (byte array)
        # message id
        message_id = Varint.from_bytes(data)
        # channel
        channel = String.from_bytes(data)
        # data
        data = ByteArray.from_bytes(data)
        return cls(message_id, channel, data)
