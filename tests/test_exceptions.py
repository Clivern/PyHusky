# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""
from __future__ import print_function
from pyhusky.exceptions import PyHuskyError
import unittest


class TestExceptionMethods(unittest.TestCase):

    def test_error(self):
        try:
            raise PyHuskyError('Error raised with %s' % 'dynamic data')
        except Exception as e:
            self.assertEqual(e.error_info, 'Error raised with dynamic data')


if __name__ == '__main__':
    unittest.main()