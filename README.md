# SFC2ICE - A tool to convert .SFC files into .ICE/.BIN packages for the SNES SHVC IS-Debugger

A very simple tool that allows to convert flat, headerless .SFC rom files to file packages for use on the IS-Debugger hardware.

It works by extracting portions of the rom file and composing a viable .ICE file to load binary blocks to appropriate addresses corresponding to the various memory pages for access by the 65816 in the IS-Debugger.

The tool does not automatically distinguish between lorom and hirom layouts, so a command line option is provided to set the address space layout of the output .ICE/.BIN files.
