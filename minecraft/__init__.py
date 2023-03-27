"""
minecraft.py
~~~~~

A Python library for Minecraft clients.

:copyright: (c) 2023-present plun1331
:license: BSD 3-Clause, see LICENSE for more details.
"""

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
__version__ = "0.0.0a1"

logging.getLogger(__name__).addHandler(logging.NullHandler())
