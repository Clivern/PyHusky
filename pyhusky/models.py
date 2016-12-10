# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""
import pymysql.cursors
from .exceptions import PyHuskyError


class MySQLModel(object):
    """MySQL Model Module"""

    _db={
        'host': '127.0.0.1',
        'username': 'root',
        'password': '',
        'database': 'pyhusky'
    }

    _tables={
        'prefix': 'ph_',
        'users_table': False,
        'users_table_id': False,
        'roles_table': 'roles',
        'permissions_table': 'permissions',
        'permission_role_table': 'permission_role',
        'role_user_table': 'role_user',
        'permission_user_table': 'permission_user'
    }

    def __init__(self, db={}, tables={}):
        """Set Database Configs and Tables

            Args:
                db: A list of database configs
                tables: A list of tables configs

        """
        for key in db:
            self._db[key] = db[key]

        for key in tables:
            self._tables[key] = tables[key]

        self._connect()

    def has_role(self, user_id, role_name, role_id=False):
        pass

    def has_permission(self, user_id, permission_name, permission_id=False):
        pass

    def get_user_roles(self, user_id):
        pass

    def get_user_permissions(self, user_id):
        pass

    def get_role(self, role_name, role_id=False):
        pass

    def get_roles(self):
        pass

    def get_permission(self, permission_name, permission_id=False):
        pass

    def get_permissions(self):
        pass

    def add_role(self, role):
        pass

    def add_roles(self, roles):
        pass

    def add_permission(self, permission):
        pass

    def add_permissions(self, permissions):
        pass

    def update_role(self, role, where):
        pass

    def update_permissions(self, role, where):
        pass

    def update_user_roles(self, user_id, roles):
        pass

    def update_user_permissions(self, user_id, permissions):
        pass

    def delete_user_role(self, user_id, role_name, role_id=False):
        pass

    def delete_user_permission(self, user_id, permission_name, permission_id=False):
        pass

    def delete_role(self, role_name, role_id=False):
        pass

    def delete_permission(self, permission_name, permission_id=False):
        pass

    def _table_exists(self, table_name):
        """Check if Tables Exist

            Args:
                table_name: a table name to check
        """
        with self._connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE '" + table_name +"';")
        self._connection.commit()
        for row in cursor:
            return table_name in row.values()

    def _connect(self):
        """Connect to Database"""
        try:
            self._connection = pymysql.connect(host=self._db['host'], user=self._db['username'], password=self._db['password'], db=self._db['database'], charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            raise PyHuskyError('Error! Cann\'t Connect to Database \'%s\'' % self._db['database'])


    def close(self):
        """Close Database Connection"""
        self._connection.close()

    def _query(self, query):
        """Run MySQL Query

            Args:
                query: MySQL query to execute
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query)
        self._connection.commit()

class SQLLiteModel(object):
    """SQLLite Model Module"""
    pass


class PostgreSQLModel(object):
    """PostgreSQL Model Module"""
    pass