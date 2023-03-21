"""
minecraft.packets
~~~~~~~~~~~~~

Contains all the packets used in the Minecraft protocol, as documented at https://wiki.vg/Protocol.

:copyright: (c) 2023-present plun1331
:license: BSD 3-Clause, see LICENSE for more details.
"""

from typing import Literal
from .base import *
from .handshake_serverbound import *
from .login_clientbound import *
from .login_serverbound import *
from .play_clientbound import *
from .play_serverbound import *
from .status_clientbound import *
from .status_serverbound import *

PACKETS_CLIENTBOUND = {}
PACKETS_SERVERBOUND = {}

for obj in dict(globals()).values():
    if isinstance(obj, type) and issubclass(obj, Packet):
        if obj.bound_to == "client":
            PACKETS_CLIENTBOUND[obj.packet_id] = obj
        else:
            PACKETS_SERVERBOUND[obj.packet_id] = obj

def get_packet(data: BytesIO, *, bound: Literal["client", "server"] = "client") -> type[Packet]:
    packet_id = Varint.from_bytes(data).value
    if bound == "client":
        return PACKETS_CLIENTBOUND[packet_id].from_bytes(data)
    else:
        return PACKETS_SERVERBOUND[packet_id].from_bytes(data)