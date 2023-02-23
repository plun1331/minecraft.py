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

    def __repr__(self) -> str:
        return f"Disconnected(reason={self.reason!r})"

    def __str__(self) -> str:
        return str(self.reason)


class EncryptionRequest(Packet):
    """
    Sent by the server to request encryption.
    
    Packet ID: 0x01
    State: Login
    Bound To: Client
    """
    id = 0x01

    def __init__(self, server_id: str, public_key: bytes, verify_token: bytes) -> None:
        self.server_id = server_id
        self.public_key = public_key
        self.verify_token = verify_token

    def __bytes__(self) -> bytes:
        public_key_length = Varint(len(self.public_key))
        verify_token_length = Varint(len(self.verify_token))
        return bytes(self.id) + bytes(self.server_id) + bytes(public_key_length) + self.public_key + bytes(
            verify_token_length
            ) + self.verify_token

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "EncryptionRequest":
        # Fields: server_id (string), public key length (varint),
        # public_key (byte array), verify token length (varing), verify_token (byte array)
        # server id
        server_id = String.from_bytes(data)
        # public key length
        public_key_length = Varint.from_bytes(data)
        # public key
        public_key = data.read(public_key_length)
        # verify token length
        verify_token_length = Varint.from_bytes(data)
        # verify token
        verify_token = data.read(verify_token_length)
        return cls(server_id, public_key, verify_token)

    def __repr__(self) -> str:
        return f"EncryptionRequest(server_id={self.server_id!r}, public_key={self.public_key!r}, verify_token={self.verify_token!r})"


class LoginSuccess(Packet):
    """
    Sent by the server to indicate that the client has successfully logged in.
    
    Packet ID: 0x02
    State: Login
    Bound To: Client
    """
    id = 0x02

    def __init__(self, uuid: str, username: str, properties: list[Property]) -> None:
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
        property_count = Varint.from_bytes(data)
        # properties
        properties = []
        for _ in range(property_count):
            properties.append(Property.from_bytes(data))
        return cls(uuid, username, properties)

    def __repr__(self) -> str:
        return f"LoginSuccess(uuid={self.uuid!r}, username={self.username!r} properties={self.properties!r})"


class SetCompression(Packet):
    """
    Sent by the server to indicate that the client should use compression.
    
    Packet ID: 0x03
    State: Login
    Bound To: Client
    """
    id = 0x03

    def __init__(self, threshold: int) -> None:
        self.threshold = threshold

    def __bytes__(self) -> bytes:
        return bytes(self.id) + bytes(Varint(self.threshold))

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "SetCompression":
        # Fields: threshold (varint)
        # threshold
        threshold = Varint.from_bytes(data)
        return cls(threshold)

    def __repr__(self) -> str:
        return f"SetCompression(threshold={self.threshold!r})"


class LoginPluginRequest(Packet):
    """
    Used to implement a custom handshaking flow together with Login Plugin Response.
    Our client should always respond that it hasn't understood the request.
    
    Packet ID: 0x04
    State: Login
    Bound To: Client
    """
    id = 0x04

    def __init__(self, message_id: int, channel: str, data: bytes) -> None:
        self.message_id = message_id
        self.channel = channel
        self.data = data

    def __bytes__(self) -> bytes:
        return bytes(self.id) + bytes(Varint(self.message_id)) + bytes(self.channel) + bytes(ByteArray(self.data))

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

    def __repr__(self) -> str:
        return f"LoginPluginRequest(message_id={self.message_id!r}, channel={self.channel!r}, data={self.data!r})"


class LoginStart(Packet):
    """
    Sent by the client to start the login process.

    Packet ID: 0x00
    State: Login
    Bound To: Server
    """
    id = 0x00

    def __init__(self, username: String, uuid: UUID | None) -> None:
        self.username: String = username
        self.uuid: UUID | None = uuid

    @property
    def uuid_set(self) -> bool:
        return self.uuid is not None

    def __bytes__(self) -> bytes:
        res = bytes(self.id) + bytes(self.username) + bytes(Boolean(self.uuid_set))
        if self.uuid_set:
            res += bytes(self.uuid)
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "LoginStart":
        # Fields: username (string), uuid set (boolean), uuid (uuid)
        # username
        username = String.from_bytes(data)
        # uuid set
        uuid_set = Boolean.from_bytes(data)
        # uuid
        uuid = None
        if uuid_set:
            uuid = UUID.from_bytes(data)
        return cls(username, uuid)

    def __repr__(self) -> str:
        return f"LoginStart(username={self.username!r}, uuid={self.uuid!r})"


class EncryptionResponse(Packet):
    """
    Sent by the client to respond to the encryption request.
    
    Packet ID: 0x01
    State: Login
    Bound To: Server
    """
    id = 0x01

    def __init__(self, shared_secret: ByteArray, verify_token: ByteArray) -> None:
        self.shared_secret: ByteArray = shared_secret
        self.verify_token: ByteArray = verify_token

    def __bytes__(self) -> bytes:
        shared_secret_length = self.shared_secret.length
        verify_token_length = self.verify_token.length
        return bytes(self.id) + bytes(shared_secret_length) + self.shared_secret + bytes(
            verify_token_length
            ) + self.verify_token

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "EncryptionResponse":
        # Fields: shared secret length (varint), shared secret (byte array), verify token length (varint), verify token (byte array)
        # shared secret length
        shared_secret_length = Varint.from_bytes(data)
        # shared secret
        shared_secret = ByteArray.from_bytes(data, shared_secret_length)
        # verify token length
        verify_token_length = Varint.from_bytes(data)
        # verify token
        verify_token = ByteArray.from_bytes(data, verify_token_length)
        return cls(shared_secret, verify_token)

    def __repr__(self) -> str:
        return f"EncryptionResponse(shared_secret={self.shared_secret!r}, verify_token={self.verify_token!r})"


class LoginPluginResponse(Packet):
    """
    Sent in response to a plugin message request.
    Our client should always respond with a `successful=False` with no further payload.
    
    Packet ID: 0x02
    State: Login
    Bound To: Server
    """
    id = 0x02

    def __init__(self, message_id: Varint, successful: Boolean, data: ByteArray | None = None) -> None:
        self.message_id: int = message_id
        self.successful: Boolean = successful
        self.data: ByteArray | None = data

    def __bytes__(self) -> bytes:
        res = bytes(self.id) + bytes(self.message_id) + bytes(self.successful)
        if self.successful:
            res += bytes(self.data)
        return res

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "LoginPluginResponse":
        # Fields: message id (varint), successful (boolean), data (byte array)
        # message id
        message_id = Varint.from_bytes(data)
        # successful
        successful = Boolean.from_bytes(data)
        # data
        if successful:
            data = ByteArray.from_bytes(data)
        else:
            data = None
        return cls(message_id, successful, data)

    def __repr__(self) -> str:
        return f"LoginPluginResponse(message_id={self.message_id!r}, successful={self.successful!r}, data={self.data!r})"
