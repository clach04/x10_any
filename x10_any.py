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
