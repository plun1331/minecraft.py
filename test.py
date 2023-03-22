import logging

import minecraft
import asyncio
from io import BytesIO

logging.basicConfig(level=logging.DEBUG)

class Client(minecraft.Client):
    async def setup(self):
        await self.microsoft_auth("1fbdf10d-d4e5-4716-b990-7ada9610a5d3")

client = Client()

client.run("mcsl.savermc.net", 25565)