import logging

import minecraft

logging.basicConfig(level=logging.DEBUG)


class Client(minecraft.Client):
    async def setup(self):
        await self.microsoft_auth("CLIENT_ID")


client = Client()

client.run("localhost", 25565)
