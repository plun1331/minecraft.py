"""
minecraft.py
~~~~~

A Python library for Minecraft clients.

:copyright: (c) 2023-present plun1331
:license: BSD 3-Clause, see LICENSE for more details.
"""

from typing import NamedTuple
import logging

from .client import *
from .datatypes import *
from .enums import *
from .networking import *
from .packets import *

__title__ = "minecraft.py"
__author__ = "plun1331"
__license__ = "BSD 3-Clause"
__copyright__ = "Copyright 2023-present plun1331"
__version__ = "0.0.0-alpha"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


try:
    releaselevel = str(__version__.split("-")[1].split(".")[0])
except IndexError:
    releaselevel = "final"
try:
    serial = int(__version__.split("-")[1].split(".")[1])
except IndexError:
    serial = 0

version_info = VersionInfo(
    major=int(__version__.split(".", maxsplit=1)[0]),
    minor=int(__version__.split(".", maxsplit=2)[1]),
    micro=int(__version__.split("-", maxsplit=3)[0].split(".")[2]),
    releaselevel=releaselevel,
    serial=serial,
)


logging.getLogger(__name__).addHandler(logging.NullHandler())
