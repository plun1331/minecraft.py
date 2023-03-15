"""
MCPy Packets
~~~~~~~~~~~~~

Contains all the packets used in the Minecraft protocol, as documented at https://wiki.vg/Protocol.

:copyright: (c) 2023-present plun1331
:license: BSD 3-Clause, see LICENSE for more details.
"""

from .base import *
from .handshake import *
from .login_clientbound import *
from .login_serverbound import *
from .play_clientbound import *
from .play_serverbound import *
from .status import *
