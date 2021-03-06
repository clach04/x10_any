#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import os
import sys
from unittest import main, TestCase

import x10_any


class TestUtils(TestCase):

    def test_validate_house_code_a_upper_unicode_type(self):
        # potentially Python 2 only test
        test_value = u'A'
        canon = 'A'
        result = x10_any.normalize_housecode(test_value)
        self.assertEqual(canon, result)

    def test_validate_house_code_a_upper(self):
        test_value = 'A'
        canon = 'A'
        result = x10_any.normalize_housecode(test_value)
        self.assertEqual(canon, result)

    def test_validate_house_code_a_lower(self):
        test_value = 'a'
        canon = 'A'
        result = x10_any.normalize_housecode(test_value)
        self.assertEqual(canon, result)

    def test_validate_house_code_c_lower(self):
        test_value = 'c'
        canon = 'C'
        result = x10_any.normalize_housecode(test_value)
        self.assertEqual(canon, result)

    def test_validate_house_code_p_upper(self):
        test_value = 'P'
        canon = 'P'
        result = x10_any.normalize_housecode(test_value)
        self.assertEqual(canon, result)

    def test_validate_house_code_p_lower(self):
        test_value = 'p'
        canon = 'P'
        result = x10_any.normalize_housecode(test_value)
        self.assertEqual(canon, result)

    def test_validate_house_code_q_upper(self):
        test_value = 'Q'

        def doit():
            x10_any.normalize_housecode(test_value)
        self.assertRaises(x10_any.X10InvalidHouseCode, doit)

    def test_validate_house_code_q_lower(self):
        test_value = 'q'

        def doit():
            x10_any.normalize_housecode(test_value)
        self.assertRaises(x10_any.X10InvalidHouseCode, doit)

    def test_validate_house_code_at_sign(self):
        test_value = '@'

        def doit():
            x10_any.normalize_housecode(test_value)
        self.assertRaises(x10_any.X10InvalidHouseCode, doit)

    def test_validate_house_code_none(self):
        test_value = None

        def doit():
            x10_any.normalize_housecode(test_value)
        self.assertRaises(x10_any.X10InvalidHouseCode, doit)

    def test_validate_house_code_aa(self):
        test_value = 'aa'

        def doit():
            x10_any.normalize_housecode(test_value)
        self.assertRaises(x10_any.X10InvalidHouseCode, doit)

    def test_validate_house_code_one_str(self):
        test_value = '1'

        def doit():
            x10_any.normalize_housecode(test_value)
        self.assertRaises(x10_any.X10InvalidHouseCode, doit)

    def test_validate_house_code_one_int(self):
        test_value = 1

        def doit():
            x10_any.normalize_housecode(test_value)
        self.assertRaises(x10_any.X10InvalidHouseCode, doit)

    def test_validate_house_code_one_float(self):
        test_value = 1.0

        def doit():
            x10_any.normalize_housecode(test_value)
        self.assertRaises(x10_any.X10InvalidHouseCode, doit)

    def test_validate_house_code_one_baseexception(self):
        test_value = '1'

        # basically a complicated
        # isinstance(x10_any.X10InvalidHouseCode(), x10_any.X10BaseException)
        def doit():
            x10_any.normalize_housecode(test_value)
        self.assertRaises(x10_any.X10BaseException, doit)

    def test_validate_unit_number_1(self):
        test_value = 1
        canon = 1
        result = x10_any.normalize_unitnumber(test_value)
        self.assertEqual(canon, result)

    def test_validate_unit_number_16(self):
        test_value = 16
        canon = 16
        result = x10_any.normalize_unitnumber(test_value)
        self.assertEqual(canon, result)

    def test_validate_unit_number_negative_1(self):
        test_value = -1

        def doit():
            _ = x10_any.normalize_unitnumber(test_value)
        self.assertRaises(x10_any.X10InvalidUnitNumber, doit)

    def test_validate_unit_number_17(self):
        test_value = 17

        def doit():
            _ = x10_any.normalize_unitnumber(test_value)
        self.assertRaises(x10_any.X10InvalidUnitNumber, doit)

    def test_validate_unit_number_none(self):
        test_value = None

        def doit():
            _ = x10_any.normalize_unitnumber(test_value)
        self.assertRaises(x10_any.X10InvalidUnitNumber, doit)

    def test_validate_unit_number_a(self):
        test_value = 'a'

        def doit():
            _ = x10_any.normalize_unitnumber(test_value)
        self.assertRaises(x10_any.X10InvalidUnitNumber, doit)

    def test_validate_unit_number_1_float(self):
        test_value = 1.0
        canon = 1
        result = x10_any.normalize_unitnumber(test_value)
        self.assertEqual(canon, result)


if __name__ == "__main__":
    sys.exit(main())
