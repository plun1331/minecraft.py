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

import json
import logging

import aiohttp

from minecraft.exceptions import AuthenticationError

log = logging.getLogger(__name__)


async def start_device_code_flow(clientapp):
    flow = clientapp.initiate_device_flow(scopes=["XboxLive.signin"])
    if "user_code" not in flow:
        raise AuthenticationError(
            "Failed to create device flow.\n" + json.dumps(flow, indent=4)
        )
    print(flow["message"])
    return flow


async def get_token_with_device_code(clientapp, flow):
    result = clientapp.acquire_token_by_device_flow(flow)
    return result


async def obtain_token_with_device_code(clientapp):
    flow = await start_device_code_flow(clientapp)
    result = await get_token_with_device_code(clientapp, flow)
    return result


async def get_access_token(token):
    sess = aiohttp.ClientSession()
    xbl_payload = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={token}" if not token.startswith("d=") else token,
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT",
    }

    xbl_response = await sess.post(
        url="https://user.auth.xboxlive.com/user/authenticate", json=xbl_payload
    )
    xbl_response = await xbl_response.json()

    xbl_token = xbl_response["Token"]
    xui_uhs = xbl_response["DisplayClaims"]["xui"][0]["uhs"]

    xsts_payload = {
        "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbl_token]},
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT",
    }

    xsts_response = await sess.post(
        "https://xsts.auth.xboxlive.com/xsts/authorize", json=xsts_payload
    )
    xsts_response = await xsts_response.json()
    xsts_token = xsts_response["Token"]

    mc_payload = {"identityToken": f"XBL3.0 x={xui_uhs};{xsts_token}"}

    mc_response = await sess.post(
        "https://api.minecraftservices.com/authentication/login_with_xbox",
        json=mc_payload,
    )
    mc_response = await mc_response.json()

    mc_token = mc_response["access_token"]

    profile = await sess.get(
        "https://api.minecraftservices.com/minecraft/profile",
        headers={"Authorization": f"Bearer {mc_token}"},
    )
    profile = await profile.json()

    await sess.close()
    return mc_token, profile["id"], profile["name"]


async def microsoft_auth(client_id: str) -> tuple[str, str, str]:
    try:
        import msal
    except ImportError as exc:
        raise RuntimeError("msal must be installed to use Microsoft authentication.") from exc
    log.debug("Starting Microsoft authentication flow with client ID %s", client_id)
    clientapp = msal.PublicClientApplication(
        client_id,
        authority="https://login.microsoftonline.com/consumers",
    )
    token = await obtain_token_with_device_code(clientapp)
    if "access_token" in token:
        try:
            auth_token, uuid, name = await get_access_token(token["access_token"])
        except Exception as e:
            raise AuthenticationError(str(e), correlation_id=token.get('correlation_id')) from e
    else:
        raise AuthenticationError(
            f"{token.get('error')}: {token.get('error_description')}",
            correlation_id=token.get('correlation_id')
        )
    return name, uuid, auth_token
