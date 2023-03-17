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

from .base import Packet
from ..datatypes import *


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
        res = bytes(self.id) + bytes(self.username) + \
            bytes(Boolean(self.uuid_set))
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


class EncryptionResponse(Packet):
    """
    Sent by the client to respond to the encryption request.

    Packet ID: 0x01
    State: Login
    Bound To: Server
    """

    packet_id = 0x01

    def __init__(self, shared_secret: ByteArray, verify_token: ByteArray) -> None:
        self.shared_secret: ByteArray = shared_secret
        self.verify_token: ByteArray = verify_token

    def __bytes__(self) -> bytes:
        shared_secret_length = len(self.shared_secret)
        verify_token_length = len(self.verify_token)
        return (
            self.packet_id.to_bytes(1, "big")
            + bytes(Varint(shared_secret_length))
            + bytes(self.shared_secret)
            + bytes(Varint(verify_token_length))
            + bytes(self.verify_token)
        )

    @classmethod
    def from_bytes(cls, data: BytesIO) -> "EncryptionResponse":
        # Fields: shared secret length (varint), shared secret (byte array),
        # verify token length (varint), verify token (byte array)
        # shared secret length
        shared_secret_length = Varint.from_bytes(data).value
        # shared secret
        shared_secret = ByteArray.from_bytes(data, length=shared_secret_length)
        # verify token length
        verify_token_length = Varint.from_bytes(data).value
        # verify token
        verify_token = ByteArray.from_bytes(data, length=verify_token_length)
        return cls(shared_secret, verify_token)


class LoginPluginResponse(Packet):
    """
    Sent in response to a plugin message request.
    Our client should always respond with a `successful=False` with no further payload.

    Packet ID: 0x02
    State: Login
    Bound To: Server
    """

    packet_id = 0x02

    def __init__(
        self, message_id: Varint, successful: Boolean, data: ByteArray | None = None
    ) -> None:
        self.message_id: Varint = message_id
        self.successful: Boolean = successful
        self.data: ByteArray | None = data

    def __bytes__(self) -> bytes:
        res = (
            self.packet_id.to_bytes(1, "big")
            + bytes(self.message_id)
            + bytes(self.successful)
        )
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
