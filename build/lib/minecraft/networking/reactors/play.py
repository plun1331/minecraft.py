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
from ...datatypes import Boolean, ByteArray
from ...enums import State
from ...exceptions import DisconnectError
from ...packets import (
    KeepAliveClientbound,
    KeepAliveServerbound,
    Ping,
    Pong,
    DisconnectPlay,
)

log = logging.getLogger(__name__)


class PlayReactor(Reactor):
    """
    Reacts to packets sent during the play state.
    """
    @react_to(KeepAliveClientbound)
    async def keep_alive(self, packet: KeepAliveClientbound):
        await self.connection.send_packet(
            KeepAliveServerbound(id=packet.keep_alive_id)
        )

    @react_to(Ping)
    async def ping(self, packet: Ping):
        await self.connection.send_packet(Pong(id=packet.id))

    @react_to(DisconnectPlay)
    async def disconnect(self, packet: DisconnectPlay):
        log.warning("Disconnected from server during play: %s", packet.reason.json)
        await self.connection.close(error=DisconnectError(packet.reason))
    