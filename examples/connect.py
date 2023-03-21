import minecraft
import asyncio
import logging

client = minecraft.Client()


logging.basicConfig(level=logging.INFO)


async def main():
    await client.microsoft_auth("CLIENT_ID")
    await client.connect("IP", 25565)

asyncio.run(main())
