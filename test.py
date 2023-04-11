"""
Shows how to connect a client to a Minecraft server.
"""

import logging

import minecraft

with open("client-info.log", "w") as f:
    f.write("")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
# file handler
fh = logging.FileHandler("client-info.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logging.getLogger().addHandler(fh)


class Client(minecraft.Client):
    """
    Our subclassed client.

    This allows us to add custom methods to the client,
    such as a setup method, which is being used to perform
    authentication before we connect to the server.
    """

    async def setup(self):
        # Authenticate with Microsoft
        # Replace CLIENT_ID with your own client ID from the Azure Developer Portal:
        # https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps
        await self.microsoft_auth("1fbdf10d-d4e5-4716-b990-7ada9610a5d3")


client = Client()

# Connect to the server
# Replace localhost with the IP of the server you want to connect to
client.run("simplesmp.net", 25565)
