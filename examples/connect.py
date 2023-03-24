"""
Shows how to connect a client to a Minecraft server.
"""

import logging

import minecraft

# Set up logging
logging.basicConfig(level=logging.INFO)


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
        await self.microsoft_auth("CLIENT_ID")


client = Client()

# Connect to the server
# Replace localhost with the IP of the server you want to connect to
client.run("localhost", 25565)
