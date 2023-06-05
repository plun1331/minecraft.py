"""
minecraft.packets
~~~~~~~~~~~~~

Contains all the packets used in the Minecraft protocol, as documented at https://wiki.vg/Protocol.

:copyright: (c) 2023-present plun1331
:license: BSD 3-Clause, see LICENSE for more details.
"""
import logging
from typing import TypeVar

from .base import *
from .handshake_serverbound import *
from .login_clientbound import *
from .login_serverbound import *
from .play_clientbound import *
from .play_serverbound import *
from .status_clientbound import *
from .status_serverbound import *
from ..exceptions import UnknownPacketError, PacketParsingError

PACKET = TypeVar("PACKET", bound=Packet)

log = logging.getLogger(__name__)

PACKETS_CLIENTBOUND: dict[State, dict[int, type[Packet]]] = {
    State.HANDSHAKE: {},
    State.STATUS: {},
    State.LOGIN: {},
    State.PLAY: {},
}
PACKETS_SERVERBOUND: dict[State, dict[int, type[Packet]]] = {
    State.HANDSHAKE: {},
    State.STATUS: {},
    State.LOGIN: {},
    State.PLAY: {},
}

for obj in dict(globals()).values():
    if isinstance(obj, type) and issubclass(obj, Packet) and obj is not Packet:
        if obj.bound_to == "client":
            PACKETS_CLIENTBOUND[obj.state][obj.packet_id] = obj
        else:
            PACKETS_SERVERBOUND[obj.state][obj.packet_id] = obj


def get_packet(
    data: bytes, *, state: State, bound: Literal["client", "server"] = "client"
) -> Packet:
    """
    Convert a packet's data into its respective packet object.

    Parameters
    ----------
    data: :class:`bytes`
        The packet's data.
    state: :class:`State`
        The state the connection was in when the packet arrived.
    bound: :class:`str`
        The destination of the packet. Can be either "client" or "server".

    Returns
    -------
    :class:`Packet`
        The packet object.

    Raises
    ------
    :exc:`ValueError`
        The bound was invalid.
    """
    original_data = data
    data = BytesIO(data)
    packet_id = Varint.from_bytes(data).value
    log.debug("Processing packet with ID %s", packet_id)
    try:
        if bound == "client":
            packet = PACKETS_CLIENTBOUND[state][packet_id]
        elif bound == "server":
            packet = PACKETS_SERVERBOUND[state][packet_id]
        else:
            raise ValueError(f"Invalid bound: {bound}")
    except KeyError as e:
        raise UnknownPacketError(packet_id, original_data) from e
    try:
        return packet.from_bytes(data)
    except Exception as e:
        raise PacketParsingError(e, packet_id, original_data) from e
