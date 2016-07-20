#! /usr/bin/env python

"""
Copyright (c) 2004 Jimmy Retzlaff

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

__version__ = 1.0

import sys
import time

import serial

# The FireCracker spec is at http://text.staticfree.info/cm17a_proto.txt
# http://www.edcheung.com/automa/rf.txt

leadInOutDelay = 0.5
bitDelay = 0.001

# contants used for translating commands into bit strings

houseCodes = dict(A=0x60, B=0x70, C=0x40, D=0x50,
                  E=0x80, F=0x90, G=0xa0, H=0xb0,
                  I=0xe0, J=0xf0, K=0xc0, L=0xd0,
                  M=0x00, N=0x10, O=0x20, P=0x30
                 )

deviceNumbers = dict(zip(map(str, range(1, 17)),
                         [
                          (0x00, 0x00), (0x00, 0x10), (0x00, 0x08), (0x00, 0x18),
                          (0x00, 0x40), (0x00, 0x50), (0x00, 0x48), (0x00, 0x58),
                          (0x04, 0x00), (0x04, 0x10), (0x04, 0x08), (0x04, 0x18),
                          (0x04, 0x40), (0x04, 0x50), (0x04, 0x48), (0x04, 0x58),
                         ]
                        )
                    )

commandCodes = {
                'ON' : 0x00, 'OFF' : 0x20,
                'DIM' : 0x98, 'BRIGHT' : 0x88,
                'ALL OFF' : 0x80, 'ALL ON' : 0x91,
                'LAMPS OFF' : 0x84, 'LAMPS ON' : 0x94
               }


# Utilities for translating and sending the bit string

def _translateCommands(commands):
    """Generate the binary strings for a comma seperated list of commands."""
    for command in commands.split(','):
        # each command results in 2 bytes of binary data
        result = [0, 0]
        device, command = command.strip().upper().split(None, 1)

        # translate the house code
        result[0] = houseCodes[device[0]]

        # translate the device number if there is one
        if len(device) > 1:
            deviceNumber = deviceNumbers[device[1:]]
            result[0] |= deviceNumber[0]
            result[1] = deviceNumber[1]

        # translate the command
        result[1] |= commandCodes[command]

        # convert 2 bytes to bit strings and yield them
        yield ' '.join(map(_strBinary, result))


def _strBinary(n):
    """Conert an integer to binary (i.e., a string of 1s and 0s)."""
    results = []
    for i in range(8):
        n, r = divmod(n, 2)
        results.append('01'[r])
    results.reverse()
    return ''.join(results)


def _sendBinaryData(port, data):
    """Send a string of binary data to the FireCracker with proper timing.

    See the diagram in the spec referenced above for timing information.
    The module level variables leadInOutDelay and bitDelay represent how
    long each type of delay should be in seconds. They may require tweaking
    on some setups.
    """
    _reset(port)
    time.sleep(leadInOutDelay)
    for digit in data:
        _sendBit(port, digit)
    time.sleep(leadInOutDelay)


def _reset(port):
    """Perform a rest of the FireCracker module."""
    _setRTSDTR(port, 0, 0)
    _setRTSDTR(port, 1, 1)


def _sendBit(port, bit):
    """Send an individual bit to the FireCracker module usr RTS/DTR."""
    if bit == '0':
        _setRTSDTR(port, 0, 1)
    elif bit == '1':
        _setRTSDTR(port, 1, 0)
    else:
        return
    time.sleep(bitDelay)
    _setRTSDTR(port, 1, 1)
    time.sleep(bitDelay)


def _setRTSDTR(port, RTS, DTR):
    """Set RTS and DTR to the requested state."""
    port.setRTS(RTS)
    port.setDTR(DTR)


# Public Interface (programmatic and command line)

def sendCommands(comPort, commands):
    """Send X10 commands using the FireCracker on comPort

    comPort should be the name of a serial port on the host platform. On
    Windows, for example, 'com1'.

    commands should be a string consisting of X10 commands separated by
    commas. For example. 'A1 On, A Dim, A Dim, A Dim, A Lamps Off'. The
    letter is a house code (A-P) and the number is the device number (1-16).
    Possible commands for a house code / device number combination are
    'On' and 'Off'. The commands 'Bright' and 'Dim' should be used with a
    house code alone after sending an On command to a specific device. The
    'All On', 'All Off', 'Lamps On', and 'Lamps Off' commands should also
    be used with a house code alone.

    # Turn on module A1
    >>> sendCommands('com1', 'A1 On')

    # Turn all modules with house code A off
    >>> sendCommands('com1', 'A All Off')

    # Turn all lamp modules with house code B on
    >>> sendCommands('com1', 'B Lamps On')

    # Turn on module A1 and dim it 3 steps, then brighten it 1 step
    >>> sendCommands('com1', 'A1 On, A Dim, A Dim, A Dim, A Bright')
    """
    try:
        port = serial.Serial(port=comPort)
        header = '11010101 10101010'
        footer = '10101101'
        for command in _translateCommands(commands):
            _sendBinaryData(port, header + command + footer)
    except serial.SerialException:
        print('Unable to open serial port %s' % comPort)
        print('')
        raise


def main(argv=None):
    """Send X10 commands when module is used from the command line.

    This uses syntax similar to sendCommands, for example:

    x10.py com2 A1 On, A2 Off, B All Off
    """
    if len(argv):
        # join all the arguments together by spaces so that quotes
        # aren't required on the command line.
        commands = ' '.join(argv)

        # the comPort is everything leading up to the first space
        comPort, commands = commands.split(None, 1)

        sendCommands(comPort, commands)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
