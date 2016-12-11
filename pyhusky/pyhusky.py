# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""
from .exceptions import PyHuskyError
from .integrations import Integrations
from .migrations import MySQLMigration
from .migrations import SQLLiteMigration
from .migrations import PostgreSQLMigration
from .models import MySQLModel
from .models import SQLLiteModel
from .models import PostgreSQLModel
from .permissions import Permissions
from .roles import Roles
from .users import Users
from .utils import Utils


class PyHusky(object):
    """PyHusky Module"""

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

    _integrations_obj=False
    _migrations_obj=False
    _models_obj=False
    _permissions_obj=False
    _roles_obj=False
    _users_obj=False
    _utils_obj=False

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

    def setup(self, tables=['roles', 'permissions', 'permission_role', 'role_user', 'permission_user']):
        """Setup Library Required Tables

            Args:
                tables: a list of tables to create
        """
        self.set_migrations_obj()
        self.migrate_up(tables)

    def config(self):
        """Config PyHusky"""
        self.set_models_obj()
        self.set_integrations_obj()
        self.set_permissions_obj()
        self.set_roles_obj()
        self.set_users_obj()
        self.set_utils_obj()

    def uninstall(self, tables=['roles', 'permissions', 'permission_role', 'role_user', 'permission_user']):
        """Drop Library Tables

            Args:
                tables: a list of tables to drop
        """
        self.set_migrations_obj()
        self.migrate_down(tables)

    def set_integrations_obj(self):
        """Set Integrations Object"""
        if self._integrations_obj == False
            self._integrations_obj = Integrations()

    def get_integrations_obj(self):
        """Set Integrations Object"""
        self.set_integrations_obj()
        return self._integrations_obj

    def set_migrations_obj(self):
        """Set Migration Object"""
        if self._migrations_obj == False
            if self._options['db_driver'] == 'mysql':
                self._migrations_obj = MySQLMigration(self._options['db'],self._options['tables'])
            else:
                raise PyHuskyError('Error! Database driver is invalid.')

    def get_migrations_obj(self):
        """Set Migration Object"""
        self.set_migrations_obj()
        return self._migrations_obj

    def set_models_obj(self):
        """Set Models Object"""
        if self._models_obj == False
            if self._options['db_driver'] == 'mysql':
                self._models_obj = MySQLModel(self._options['db'],self._options['tables'])
            else:
                raise PyHuskyError('Error! Database driver is invalid.')

    def get_models_obj(self):
        """Set Models Object"""
        self.set_models_obj()
        return self._models_obj

    def set_permissions_obj(self):
        """Set Permissions Object"""
        if self._permissions_obj == False
            self._permissions_obj = Permissions(self._models_obj)

    def get_permissions_obj(self):
        """Set Permissions Object"""
        self.set_permissions_obj()
        return self._permissions_obj

    def set_roles_obj(self):
        """Set Roles Object"""
        if self._roles_obj == False
            self._roles_obj = Roles(self._models_obj)

    def get_roles_obj(self):
        """Set Roles Object"""
        self.set_roles_obj()
        return self._roles_obj

    def set_users_obj(self):
        """Set Users Object"""
        if self._users_obj == False
            self._users_obj = Users(self._models_obj)

    def get_users_obj(self):
        """Set Users Object"""
        self.set_users_obj()
        return self._users_obj

    def set_utils_obj(self):
        """Set Utils Object"""
        if self._utils_obj == False
            self._utils_obj = Utils()

    def get_utils_obj(self):
        """Set Utils Object"""
        self.set_utils_obj()
        return self._utils_obj


    def migrate_up(self, tables):
        """Create Tables

            Args:
                tables: a list of tables to create
        """
        if 'roles' in tables:
            self._migrations_obj.create_roles_table()
        if 'permissions' in tables:
            self._migrations_obj.create_permissions_table()
        if 'permission_role' in tables:
            self._migrations_obj.create_permission_role_table()
        if 'role_user' in tables:
            self._migrations_obj.create_role_user_table()
        if 'permission_user' in tables:
            self._migrations_obj.create_permission_user_table()

        self._migrations_obj.close()

    def migrate_down(self, tables):
        """Drop Tables

            Args:
                tables: a list of tables to drop
        """
        if 'permission_user' in tables:
            self._migrations_obj.drop_permission_user_table()
        if 'role_user' in tables:
            self._migrations_obj.drop_role_user_table()
        if 'permission_role' in tables:
            self._migrations_obj.drop_permission_role_table()
        if 'roles' in tables:
            self._migrations_obj.drop_roles_table()
        if 'permissions' in tables:
            self._migrations_obj.drop_permissions_table()

        self._migrations_obj.close()
