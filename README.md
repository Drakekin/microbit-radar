The Micro:bit Radar Project
===========================

A range finding application written in Micropython for the BBC Micro:bit designed for two to five micro:bits.

It uses the radio to determine distance via the principal that messages at higher powers will travel further.

This software runs okay, although it's pushing the edge of the amount of memory available on the micro:bit. It may run out of memory in normal usage.

Use the `uflash` module to flash `echolocate.py` to two or more microbits to start.

`radar.py` is also provided as an early experiment to make a radar display for a further idea to then triangulate the position of multiple micro:bits, but given that the pure distance finder is already pushing the memory available it has been abandoned for now.

Work might continue, mostly to clean the code up.

