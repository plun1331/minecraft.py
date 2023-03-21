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
import os
import hashlib
import aiohttp
import base64
import rsa

from typing import TYPE_CHECKING

from ..packets.login_clientbound import EncryptionRequest

if TYPE_CHECKING:
    from .connection import Connection


def generate_shared_secret() -> bytes:
    """Generate a random 16-byte shared secret."""
    return os.urandom(16)


def generate_verify_token() -> bytes:
    """Generate a random 4-byte verify token."""
    return os.urandom(4)


def hexdigest(sha: hashlib._Hash) -> str:
    """Implement Minecraft's custom hexdigest function."""
    output_bytes = sha.digest()
    output_int = int.from_bytes(output_bytes, byteorder='big', signed=True)
    if output_int < 0:
        return '-' + hex(abs(output_int))[2:]
    else:
        return hex(output_int)[2:]


def load_public_key(public_key: bytes) -> rsa.PublicKey:
    key = "-----BEGIN PUBLIC KEY-----\n" + base64.b64encode(public_key).decode() + "-----END PUBLIC KEY-----"
    return rsa.PublicKey.load_pkcs1_openssl_pem(key.encode())


async def process_encryption_request(packet: EncryptionRequest, connection: Connection):
    """Process an encryption request packet."""
    server_id = packet.server_id
    server_public_key = packet.public_key
    loaded_server_public_key = load_public_key(server_public_key)
    client_shared_secret = generate_shared_secret()
    encrypted_shared_secret = rsa.encrypt(client_shared_secret, loaded_server_public_key)
    client_verify_token = generate_verify_token()
    encrypted_verify_token = rsa.encrypt(client_verify_token, loaded_server_public_key)
    # padding
    encrypted_shared_secret += b'\x00' * (128 - len(encrypted_shared_secret))
    encrypted_verify_token += b'\x00' * (128 - len(encrypted_verify_token))
    sha1 = hashlib.sha1()
    sha1.update(server_id.encode('ascii'))
    sha1.update(client_shared_secret)
    sha1.update(server_public_key)
    client_hash = hexdigest(sha1)
    async with aiohttp.ClientSession() as session:
        async with session.request("https://sessionserver.mojang.com/session/minecraft/join", data={
            "accessToken": connection.client.access_token,
            "selectedProfile": connection.client.uuid,
            "serverId": client_hash
        }) as resp:
            resp.raise_for_status()
    return {
        "shared_secret": client_shared_secret,
        "encrypted_shared_secret": encrypted_shared_secret,
        "encrypted_verify_token": encrypted_verify_token
    }


        


        