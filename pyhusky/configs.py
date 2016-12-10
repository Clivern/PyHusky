# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""
from .migrations import MySQLMigration
from .migrations import SQLLiteMigration
from .migrations import PostgreSQLMigration

from .models import MySQLModel
from .models import SQLLiteModel
from .models import PostgreSQLModel

from .exceptions import PyHuskyError

class Configs(object):
    """Configs Module"""

    _options={
        'db_driver': 'mysql',
        'db': {
            'host': '127.0.0.1',
            'username': 'root',
            'password': '',
            'database': 'pyhusky'
        },
        'tables': {
            'prefix': 'ph_',
            'users_table': False,
            'users_table_id': False,
            'roles_table': 'roles',
            'permissions_table': 'permissions',
            'permission_role_table': 'permission_role',
            'role_user_table': 'role_user',
            'permission_user_table': 'permission_user'
        }
    }

    def __init__(self, options):
        """Init Class Instance and Update Options

            Args:
                options: A list of library options

        """
        if 'db_driver' in options:
            self._options['db_driver'] = options['db_driver']
        if 'db' in options:
            for key in options['db']:
                self._options['db'][key] = options['db'][key]
        if 'tables' in options:
            for key in options['tables']:
                self._options['tables'][key] = options['tables'][key]

    def migrate_up(self, tables):
        """Create Tables

            Args:
                tables: a list of tables to create
        """
        if self._options['db_driver'] == 'mysql':
            migration = MySQLMigration(self._options['db'],self._options['tables'])

            if 'roles' in tables:
                migration.create_roles_table()
            if 'permissions' in tables:
                migration.create_permissions_table()
            if 'permission_role' in tables:
                migration.create_permission_role_table()
            if 'role_user' in tables:
                migration.create_role_user_table()
            if 'permission_user' in tables:
                migration.create_permission_user_table()

            migration.close()

    def migrate_down(self, tables):
        """Drop Tables

            Args:
                tables: a list of tables to drop
        """
        if self._options['db_driver'] == 'mysql':
            migration = MySQLMigration(self._options['db'],self._options['tables'])

            if 'permission_user' in tables:
                migration.drop_permission_user_table()
            if 'role_user' in tables:
                migration.drop_role_user_table()
            if 'permission_role' in tables:
                migration.drop_permission_role_table()
            if 'roles' in tables:
                migration.drop_roles_table()
            if 'permissions' in tables:
                migration.drop_permissions_table()

            migration.close()

        else:
            raise PyHuskyError('Error! Database driver is invalid.')

    def get_model(self):
        """Get Database Used Model"""
        if self._options['db_driver'] == 'mysql':
            model = MySQLModel(self._options['db'],self._options['tables'])

            return model
        else:
            raise PyHuskyError('Error! Database driver is invalid.')
