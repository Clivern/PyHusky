# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""


__version__ = "1.0.0"


def read_file(file_path):
    content = ""
    with open(file_path) as f:
        content = f.read()
    return content
