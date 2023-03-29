"""
minecraft.networking.reactors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Processes and reacts to packets.

:copyright: (c) 2023-present plun1331
:license: BSD 3-Clause, see LICENSE for more details.
"""
from .base import Reactor, REACTOR, react_to
from .login import LoginReactor
from .play import PlayReactor
from ...enums import State

REACTORS: dict[State, type[Reactor]] = {
    State.HANDSHAKE: None,
    State.STATUS: None,
    State.LOGIN: LoginReactor,
    State.PLAY: PlayReactor,
}
