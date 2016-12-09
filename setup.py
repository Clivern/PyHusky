# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""

from setuptools import setup
from pyhusky import __version__
from pyhusky import read_file


setup(
    name="pyhusky",
    version=__version__,
    author="Clivern",
    author_email="hello@clivern.com",
    description="Python Role Based Permissions Library",
    license="MIT",
    keywords="role,acl,permissions",
    url="http://clivern.github.io/pyhusky/",
    packages=['pyhusky'],
    long_description=read_file('README.md'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ],
)
