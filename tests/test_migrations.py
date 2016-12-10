# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""
from __future__ import print_function
from pyhusky.migrations import MySQLMigration
import unittest


class TestExceptionMethods(unittest.TestCase):

    def test_migration(self):
        mig = MySQLMigration({
            'host': '127.0.0.1',
            'username': 'root',
            'password': '',
            'database': 'pyhusky'
        },{})
        self.assertEqual(mig.create_roles_table(), None)
        self.assertEqual(mig.create_permissions_table(), None)
        self.assertEqual(mig.create_permission_role_table(), None)
        self.assertEqual(mig.create_role_user_table(), None)
        self.assertEqual(mig.create_permission_user_table(), None)

        self.assertEqual(mig.drop_permission_user_table(), None)
        self.assertEqual(mig.drop_role_user_table(), None)
        self.assertEqual(mig.drop_permission_role_table(), None)
        self.assertEqual(mig.drop_roles_table(), None)
        self.assertEqual(mig.drop_permissions_table(), None)


if __name__ == '__main__':
    unittest.main()
