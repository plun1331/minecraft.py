import asyncio
import logging

import minecraft

client = minecraft.Client()


logging.basicConfig(level=logging.INFO)


async def main():
    await client.microsoft_auth("CLIENT_ID")
    await client.connect("IP", 25565)


asyncio.run(main())
