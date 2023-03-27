Packets
=======

Every packet in the Minecraft protocol is implemented here.

All packets inherit from one base class, :class:`.Packet`.

.. toctree::
    :maxdepth: 1

    handshake
    login
    status
    play


Packet
------

.. currentmodule:: minecraft.packets

.. autoclass:: Packet
    :members:

    .. autoattribute:: packet_id
        :annotation: = The packet's ID

    .. autoattribute:: state
        :annotation: = The state the packet is used in

    .. autoattribute:: bound_to
        :annotation: = The direction the packet is sent in

.. autofunction:: get_packet
