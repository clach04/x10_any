#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import os
import sys
from unittest import main, TestCase

# import x10_any


class TestUtils(TestCase):
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

    def test_validate_house_code_p_upper(self):
        test_value = 'P'
        canon = 'A'
        result = x10_any.normalize_housecode(test_value)
        self.assertEqual(canon, result)

    def test_validate_house_code_p_lower(self):
        test_value = 'p'
        canon = 'A'
        result = x10_any.normalize_housecode(test_value)
        self.assertEqual(canon, result)

    def test_validate_house_code_q_upper(self):
        test_value = 'Q'
        canon = 'A'

        def doit():
            x10_any.normalize_housecode(test_value)
        self.failUnlessRaises(ValueError, doit)  # not sure I see the need for a x10_any.??Exception

    def test_validate_house_code_q_lower(self):
        test_value = 'q'
        canon = 'A'

        def doit():
            x10_any.normalize_housecode(test_value)
        self.failUnlessRaises(ValueError, doit)  # not sure I see the need for a x10_any.??Exception


if __name__ == "__main__":
    sys.exit(main())
