# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""


class PyHuskyError(Exception):
    """Validation Custom Exceptions module"""

    def __init__(self, error_info):
        Exception.__init__(self, "PyHusky exception was raised")
        self.error_info = error_info