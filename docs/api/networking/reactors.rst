.. currentmodule:: minecraft.networking.reactors

Reactors
=========

A reactor is a class used by the :class:`.Connection` to handle incoming packets, 
while also forcing the read loop to wait until processing of the packet is complete.

This is useful in cases like :class:`.SetCompression`, in which the next packet will be compressed,
and the :class:`.Connection` needs to know that before recieving it.

These are mostly used by the library and shouldn't need to be overriden by you, the developer, 
however, you can still override their default behavior by updating :data:`REACTORS` with your own :class:`Reactor`.

.. data:: REACTORS

    A dictionary mapping connection states to reactors. (:class:`dict`\[:class:`.State`, :class:`Reactor`\])

.. autoclass:: Reactor
    :members:

.. autofunction:: react_to

Login
---------

.. autoclass:: LoginReactor
    :members:
    :undoc-members:
