#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import os
import sys


class X10BaseException(Exception):
    '''Base X10 any exception'''


class X10InvalidHouseCode(X10BaseException):
    '''Invalid House Code exception'''


def normalize_housecode(house_code):
    house_code = house_code.upper()
    return house_code
