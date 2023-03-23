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

import hashlib
import os
from typing import TYPE_CHECKING

import aiohttp
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from cryptography.hazmat.primitives.serialization import load_der_public_key

from ..packets.login_clientbound import EncryptionRequest

if TYPE_CHECKING:
    from .connection import Connection


def generate_shared_secret():
    return os.urandom(16)


def create_cipher(shared_secret):
    cipher = Cipher(
        algorithms.AES(shared_secret),
        modes.CFB8(shared_secret),
        backend=default_backend(),
    )
    return cipher


def generate_verify_token() -> bytes:
    """Generate a random 4-byte verify token."""
    return os.urandom(4)


def encrypt_secret_and_token(
    public_key: bytes, shared_secret: bytes, verify_token: bytes
) -> dict:
    pubkey = load_der_public_key(public_key)
    encrypted_shared_secret = pubkey.encrypt(shared_secret, PKCS1v15())
    encrypted_verify_token = pubkey.encrypt(verify_token, PKCS1v15())
    return encrypted_shared_secret, encrypted_verify_token


def minecraft_hexdigest(sha) -> str:
    output_bytes = sha.digest()
    output_int = int.from_bytes(output_bytes, byteorder="big", signed=True)
    if output_int < 0:
        return "-" + hex(abs(output_int))[2:]
    return hex(output_int)[2:]


def generate_hash(server_id, shared_secret, public_key):
    client_hash = hashlib.sha1()
    client_hash.update(server_id.encode("utf-8"))
    client_hash.update(shared_secret)
    client_hash.update(public_key)
    return minecraft_hexdigest(client_hash)


async def process_encryption_request(packet: EncryptionRequest, connection: Connection):
    """Process an encryption request packet."""
    server_id = packet.server_id.value
    server_public_key = packet.public_key.data

    shared_secret = generate_shared_secret()
    verify_token = generate_verify_token()

    encrypted_shared_secret, encrypted_verify_token = encrypt_secret_and_token(
        server_public_key, shared_secret, verify_token
    )

    client_hash = generate_hash(server_id, shared_secret, server_public_key)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://sessionserver.mojang.com/session/minecraft/join",
            json={
                "accessToken": connection.client.access_token,
                "selectedProfile": connection.client.uuid,
                "serverId": client_hash,
            },
        ) as resp:
            resp.raise_for_status()
    return {
        "shared_secret": shared_secret,
        "encrypted_shared_secret": encrypted_shared_secret,
        "encrypted_verify_token": encrypted_verify_token,
    }
