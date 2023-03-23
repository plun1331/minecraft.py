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

import logging

from .base import react_to, Reactor
from ..encryption import create_cipher, process_encryption_request
from ... import SetCompression
from ...datatypes import Boolean, ByteArray
from ...enums import State
from ...exceptions import LoginDisconnectError
from ...packets import (
    DisconnectLogin,
    EncryptionRequest,
    EncryptionResponse,
    LoginPluginRequest,
    LoginPluginResponse,
    LoginSuccess,
)

log = logging.getLogger(__name__)


class LoginReactor(Reactor):
    @react_to(EncryptionRequest)
    async def encryption_request(self, packet: EncryptionRequest):
        encryption_data = await process_encryption_request(packet, self.connection)
        await self.connection.send_packet(
            EncryptionResponse(
                shared_secret=ByteArray(encryption_data["encrypted_shared_secret"]),
                verify_token=ByteArray(encryption_data["encrypted_verify_token"]),
            )
        )
        self.connection.shared_secret = encryption_data["shared_secret"]
        self.connection.cipher = create_cipher(self.connection.shared_secret)
        self.connection.encryptor = self.connection.cipher.encryptor()
        self.connection.decryptor = self.connection.cipher.decryptor()

    @react_to(LoginSuccess)
    async def login_success(self, packet: LoginSuccess):
        log.info("Successful login as %s", packet.username.value)
        self.connection.change_state(State.PLAY)
        self.client.uuid = packet.uuid
        self.client.username = packet.username
        self.client.properties = packet.properties

    @react_to(DisconnectLogin)
    async def disconnect_login(self, packet: DisconnectLogin):
        log.warning("Disconnected from server during login: %s", packet.reason.json)
        await self.connection.close(error=LoginDisconnectError(packet.reason))

    @react_to(LoginPluginRequest)
    async def login_plugin_request(self, packet: LoginPluginRequest):
        await self.connection.send_packet(
            LoginPluginResponse(
                message_id=packet.message_id,
                successful=Boolean(False),
            )
        )

    @react_to(SetCompression)
    async def set_compression(self, packet: SetCompression):
        log.warning(
            f"Server requested compression with threshold {packet.threshold.value}"
        )
        self.connection.compression_threshold = packet.threshold.value
        self.connection.use_compression = packet.threshold.value >= 0
