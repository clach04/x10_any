#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import os
import sys


try:
    basestring
except NameError:
    # python 3
    basestring = str


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

        print('x10_command%r' % ((house_code, unit_number, state), ))
        raise NotImplementedError()
