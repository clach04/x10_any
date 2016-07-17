#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import logging
import os
import socket
import sys


try:
    basestring
except NameError:
    # python 3
    basestring = str


version_tuple = (0, 0, 2)
version = version_string = __version__ = '%d.%d.%d' % version_tuple

logging.basicConfig()
default_logger = logging.getLogger(__name__)


class X10BaseException(Exception):
    '''Base X10 any exception'''


class X10InvalidHouseCode(X10BaseException):
    '''Invalid House Code exception'''


class X10InvalidUnitNumber(X10BaseException):
    '''Invalid Unit Number exception'''


def normalize_housecode(house_code):
    """Returns a normalized house code, i.e. upper case.
    Raises exception X10InvalidHouseCode if house code appears to be invalid
    """
    if house_code is None:
        raise X10InvalidHouseCode('%r is not a valid house code' % house_code)
    if not isinstance(house_code, basestring):
        raise X10InvalidHouseCode('%r is not a valid house code' % house_code)
    if len(house_code) != 1:
        raise X10InvalidHouseCode('%r is not a valid house code' % house_code)
    house_code = house_code.upper()
    if not ('A' <= house_code <= 'P'):
        raise X10InvalidHouseCode('%r is not a valid house code' % house_code)
    return house_code


def normalize_unitnumber(unit_number):
    """Returns a normalized unit number, i.e. integers
    Raises exception X10InvalidUnitNumber if unit number appears to be invalid
    """
    try:
        try:
            unit_number = int(unit_number)
        except ValueError:
            raise X10InvalidUnitNumber('%r not a valid unit number' % unit_number)
    except TypeError:
        raise X10InvalidUnitNumber('%r not a valid unit number' % unit_number)
    if not (1 <= unit_number <= 16):
        raise X10InvalidUnitNumber('%r not a valid unit number' % unit_number)
    return unit_number


# Mochad command constants - TODO make these an enum?
ALL_OFF = 'all_units_off'
LAMPS_OFF = 'all_lights_off'
LAMPS_ON = 'all_lights_on'
ON = 'ON'
OFF = 'OFF'

# Mappings from Mochad command to https://bitbucket.org/cdelker/python-x10-firecracker-interface/
x10_mapping = {
    ALL_OFF: 'ALL OFF',
    LAMPS_OFF: 'Lamps Off',
    LAMPS_ON: 'Lamps On',
}


class X10Driver(object):
    """Base class for a simple, one-shot X10 command driver"""

    def __init__(self, device_address):
        self.device_address = device_address

    def close(self):
        # what ever needs to be done
        # then cleanup
        # if called multiple times, be silent
        if hasattr(self, 'device_address'):
            del self.device_address

    def __del__(self):
        self.close()

    def x10_command(self, house_code, unit_number, state):
        """Send X10 command to ??? unit.

        @param house_code (A-P) - example='A'
        @param unit_number (1-16)- example=1 (or None to impact entire house code)
        @param state - Mochad command/state, See
                https://sourceforge.net/p/mochad/code/ci/master/tree/README
                examples=OFF, 'OFF', 'ON', ALL_OFF, 'all_units_off', 'xdim 128', etc.

        Examples:
            x10_command('A', '1', ON)
            x10_command('A', '1', OFF)
            x10_command('A', '1', 'ON')
            x10_command('A', '1', 'OFF')
            x10_command('A', None, ON)
            x10_command('A', None, OFF)
            x10_command('A', None, 'all_lights_off')
            x10_command('A', None, 'all_units_off')
            x10_command('A', None, ALL_OFF)
            x10_command('A', None, 'all_lights_on')
            x10_command('A', 1, 'xdim 128')
        """

        house_code = normalize_housecode(house_code)
        if unit_number is not None:
            unit_number = normalize_unitnumber(unit_number)
        # else command is intended for the entire house code, not a single unit number
        # TODO normalize/validate state

        return self._x10_command(house_code, unit_number, state)

    def _x10_command(self, house_code, unit_number, state):
        """Real implementation"""
        print('x10_command%r' % ((house_code, unit_number, state), ))
        raise NotImplementedError()


def netcat(hostname, port, content, log=None):
    log = log or default_logger

    def read_all_from_sock(s):
        buff = []
        while True:
            data = s.recv(1024)
            if data:
                buff.append(data)
            else:
                break
        return b''.join(buff)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.debug('Trying connection to: %s:%s', hostname, port)
        s.connect((hostname, port))

        log.debug('Connected to: %s:%s', hostname, port)
        received_data_before_send = s.recv(1024)
        s.sendall(b"%s\n" % content)  # FIXME newline?
        log.debug('sent: %r', content)
        s.shutdown(socket.SHUT_WR)

        received_data_after_send = read_all_from_sock(s)
        log.debug('Received: %r', received_data_after_send)
        s.close()
        log.debug('Connection closed.')
        return (received_data_before_send, received_data_after_send)
    except Exception as ex:
        log.error('ERROR: %r', ex)
        raise ex



def to_bytes(in_str):
    # could choose to only encode for Python 3+
    # could simple use latin1
    return in_str.encode('utf-8')


class MochadDriver(X10Driver):
    """X10 command driver for Mochad (or compatible) server.
    See:
      * https://sourceforge.net/projects/mochad/ for CM15A RF
        (radio frequency) and PL (power line) controller and
        the CM19A RF controller
      * https://bitbucket.org/clach04/mochad_firecracker/
        works under Windows and Linux and can control CM17A serial Firecracker

    NOTE This implementation opens the socket and then closes it for each command.
    TODO implement status support, see https://github.com/zonyl/pytomation/blob/master/pytomation/interfaces/mochad.py
    """

    def __init__(self, device_address=None, default_type=None):
        """
        @param device_address - Optional tuple of (host_address, host_port).
            Defaults to localhost:1099
        @param default_type - Option type of device to send command,
            'rf'  or 'pl'. Defaults to 'rf'
        """
        self.device_address = device_address or ('localhost', 1099)
        self.default_type = default_type or 'rf'
        self.default_type = to_bytes(self.default_type)

    def _x10_command(self, house_code, unit_number, state):
        """Real implementation"""

        #log = log or default_logger
        log = default_logger
        if state.startswith('xdim') or state.startswith('dim') or state.startswith('bright'):
            raise NotImplementedError('xdim/dim/bright %r' % ((house_code, unit_num, state), ))

        if unit_number is not None:
            house_and_unit = '%s%d' % (house_code, unit_number)
        else:
            raise NotImplementedError('mochad all ON/OFF %r' % ((house_code, unit_number, state), ))
            house_and_unit = house_code

        house_and_unit = to_bytes(house_and_unit)
        state = to_bytes(state)
        # TODO normalize/validate state
        mochad_cmd = b"%s %s %s\n" % (self.default_type, house_and_unit, state)
        log.debug('mochad send: %r', mochad_cmd)
        mochad_host, mochad_port = self.device_address
        result = netcat(mochad_host, mochad_port, mochad_cmd)
        log.debug('mochad received: %r', result)
