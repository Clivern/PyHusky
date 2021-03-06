# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""
import pymysql.cursors
#from .exceptions import PyHuskyError
import datetime

# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

"""
get_user_roles

mysql> describe ph_roles;
+--------------+------------------+------+-----+---------------------+----------------+
| Field        | Type             | Null | Key | Default             | Extra          |
+--------------+------------------+------+-----+---------------------+----------------+
| id           | int(10) unsigned | NO   | PRI | NULL                | auto_increment |
| name         | varchar(255)     | NO   | UNI | NULL                |                |
| display_name | varchar(255)     | YES  |     | NULL                |                |
| description  | varchar(255)     | YES  |     | NULL                |                |
| created_at   | timestamp        | NO   |     | 0000-00-00 00:00:00 |                |
| updated_at   | timestamp        | NO   |     | 0000-00-00 00:00:00 |                |
| enabled      | tinyint(1)       | NO   |     | 0                   |                |
+--------------+------------------+------+-----+---------------------+----------------+
7 rows in set (0.00 sec)

SELECT ph_roles.* FROM ph_roles join ph_role_user on ph_role_user.role_id = ph_roles.id WHERE ph_role_user.user_id = {user_id}
SELECT ph_permissions.* FROM ph_permissions join ph_permission_user on ph_permission_user.permission_id = ph_permissions.id WHERE ph_permission_user.user_id = {user_id}
SELECT ph_permissions.* FROM ph_permissions join ph_permission_role on ph_permission_role.permission_id = ph_permissions.id WHERE ph_permission_role.role_id IN ({roles})

INSERT INTO ph_roles (name, display_name, description, created_at, updated_at, enabled) VALUES ();


mysql> describe ph_role_user;
+---------+------------------+------+-----+---------+-------+
| Field   | Type             | Null | Key | Default | Extra |
+---------+------------------+------+-----+---------+-------+
| user_id | int(10) unsigned | NO   | PRI | NULL    |       |
| role_id | int(10) unsigned | NO   | PRI | NULL    |       |
+---------+------------------+------+-----+---------+-------+
DELETE FROM ph_role_user WHERE role_id={role_id} AND user_id={user_id}


2 rows in set (0.00 sec)
mysql> select users.name, programs.name from linker
    -> join users on users.id = linker.user_id
    -> join programs on programs.id = linker.program_id;


SELECT * FROM ph_role_user WHERE user_id=%s AND role_id=%
SELECT ph_roles.id, ph_roles.display_name from ph_roles join ph_role_user on ph_role_user.role_id  = ph_roles.id WHERE ph_roles.name = {role_name} AND ph_role_user.user_id = {user_id}

mysql> describe ph_permissions;
+--------------+------------------+------+-----+---------------------+----------------+
| Field        | Type             | Null | Key | Default             | Extra          |
+--------------+------------------+------+-----+---------------------+----------------+
| id           | int(10) unsigned | NO   | PRI | NULL                | auto_increment |
| name         | varchar(255)     | NO   | UNI | NULL                |                |
| display_name | varchar(255)     | YES  |     | NULL                |                |
| description  | varchar(255)     | YES  |     | NULL                |                |
| created_at   | timestamp        | NO   |     | 0000-00-00 00:00:00 |                |
| updated_at   | timestamp        | NO   |     | 0000-00-00 00:00:00 |                |
| enabled      | tinyint(1)       | NO   |     | 0                   |                |
+--------------+------------------+------+-----+---------------------+----------------+
7 rows in set (0.01 sec)

mysql> describe ph_permission_user;
+---------------+------------------+------+-----+---------+-------+
| Field         | Type             | Null | Key | Default | Extra |
+---------------+------------------+------+-----+---------+-------+
| permission_id | int(10) unsigned | NO   | PRI | NULL    |       |
| user_id       | int(10) unsigned | NO   | PRI | NULL    |       |
+---------------+------------------+------+-----+---------+-------+
2 rows in set (0.00 sec)
DELETE FROM ph_permission_user WHERE permission_id={permission_id} AND user_id={user_id}

mysql> describe ph_permission_role;
+---------------+------------------+------+-----+---------+-------+
| Field         | Type             | Null | Key | Default | Extra |
+---------------+------------------+------+-----+---------+-------+
| permission_id | int(10) unsigned | NO   | PRI | NULL    |       |
| role_id       | int(10) unsigned | NO   | PRI | NULL    |       |
+---------------+------------------+------+-----+---------+-------+
2 rows in set (0.00 sec)

SELECT ph_permission_role.role_id FROM ph_permission_role join ph_permissions ON ph_permissions.id=ph_permission_role.permission_id WHERE ph_permissions.id = {permission_id}
SELECT ph_permission_role.role_id FROM ph_permission_role join ph_permissions ON ph_permissions.id=ph_permission_role.permission_id WHERE ph_permissions.name = {permission_name}
name
"""
"""
INSERT INTO ph_rules (name, display_name, description, created_at, updated_at, enabled) VALUES (value1, value2, value3,...)
DELETE FROM ph_rules WHERE name=value;
UPDATE ph_rules SET display_name=value, description=value WHERE name=value;
SELECT * FROM ph_rules WHERE name=value
"""
class MySQLModel(object):
    """MySQL Model Module"""

    _db={
        'host': 'localhost',
        'username': 'root',
        'password': 'root',
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
        if role_id != False:
            query="SELECT * FROM {role_user_table} WHERE user_id={user_id} AND role_id={role_id}".format(
                role_user_table=self._tables['prefix'] + self._tables['role_user_table'],
                user_id=user_id,
                role_id=role_id
            )
        elif role_name != False:
            query="SELECT {roles_table}.id, {roles_table}.display_name FROM {roles_table} JOIN {role_user_table} ON {role_user_table}.role_id = {roles_table}.id WHERE {roles_table}.name = {role_name} AND {role_user_table}.user_id = {user_id}".format(
                role_user_table=self._tables['prefix'] + self._tables['role_user_table'],
                roles_table=self._tables['prefix'] + self._tables['roles_table'],
                user_id=user_id,
                role_name=role_name
            )
        else:
            raise PyHuskyError("Error! Invalid Method Parameters Submitted 'PyHusky_Model:has_role'")


    def role_enabled(self, role_name, role_id=False):
        if role_id != False:
            query="SELECT * FROM {roles_table} WHERE id={role_id} AND enabled=1".format(
                roles_table=self._tables['prefix'] + self._tables['roles_table'],
                role_id=role_id
            )
        elif role_name != False:
            query="SELECT * FROM {roles_table} WHERE name={role_name} AND enabled=1".format(
                roles_table=self._tables['prefix'] + self._tables['roles_table'],
                role_name=role_name
            )
        else:
            raise PyHuskyError("Error! Invalid Method Parameters Submitted 'PyHusky_Model:role_enabled'")

    def has_permission(self, user_id, permission_name, permission_id=False):
        if permission_id != False:
            query_1="SELECT * FROM {permission_user_table} WHERE user_id={user_id} AND permission_id={permission_id}".format(
                permission_user_table=self._tables['prefix'] + self._tables['permission_user_table'],
                user_id=user_id,
                permission_id=permission_id
            )
            query_2="SELECT {permission_role_table}.role_id FROM {permission_role_table} JOIN {permissions_table} ON {permissions_table}.id={permission_role_table}.permission_id WHERE {permissions_table}.id = {permission_id}".format(
                permission_role_table=self._tables['prefix'] + self._tables['permission_role_table'],
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_id=permission_id
            )

            if roles_ids != '':
                query_3="SELECT * FROM {role_user_table} WHERE user_id={user_id} AND role_id IN ({roles_ids})".format(
                    role_user_table=self._tables['prefix'] + self._tables['role_user_table'],
                    user_id=user_id,
                    roles_ids=roles_ids
                )
        elif permission_name != False:
            query_1="SELECT {permissions_table}.id, {permissions_table}.display_name FROM {permissions_table} JOIN {permission_user_table} ON {permission_user_table}.permission_id = {permissions_table}.id WHERE {permissions_table}.name = {permission_name} AND {permission_user_table}.user_id = {user_id}".format(
                permission_user_table=self._tables['prefix'] + self._tables['permission_user_table'],
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                user_id=user_id,
                permission_name=permission_name
            )
            query_2="SELECT {permission_role_table}.role_id FROM {permission_role_table} JOIN {permissions_table} ON {permissions_table}.id={permission_role_table}.permission_id WHERE {permissions_table}.name = {permission_name}".format(
                permission_role_table=self._tables['prefix'] + self._tables['permission_role_table'],
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_name=permission_name
            )

            if roles_ids != '':
                query_3="SELECT * FROM {role_user_table} WHERE user_id={user_id} AND role_id IN ({roles_ids})".format(
                    role_user_table=self._tables['prefix'] + self._tables['role_user_table'],
                    user_id=user_id,
                    roles_ids=roles_ids
                )
        else:
            raise PyHuskyError("Error! Invalid Method Parameters Submitted 'PyHusky_Model:has_permission'")


    def permission_enabled(self, permission_name, permission_id=False):
        if permission_id != False:
            query="SELECT * FROM {permissions_table} WHERE id={permission_id} AND enabled=1".format(
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_id=permission_id
            )
        elif permission_name != False:
            query="SELECT * FROM {permissions_table} WHERE name={permission_name} AND enabled=1".format(
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_name=permission_name
            )
        else:
            raise PyHuskyError("Error! Invalid Method Parameters Submitted 'PyHusky_Model:permission_enabled'")


    def get_user_roles(self, user_id):
        query="SELECT {roles_table}.* FROM {roles_table} JOIN {role_user_table} ON {role_user_table}.role_id = {roles_table}.id WHERE {role_user_table}.user_id = {user_id}".format(
            roles_table=self._tables['prefix'] + self._tables['roles_table'],
            role_user_table=self._tables['prefix'] + self._tables['role_user_table'],
            user_id=user_id
        )

    def get_user_permissions(self, user_id):
        query_1="SELECT {roles_table}.* FROM {roles_table} JOIN {role_user_table} ON {role_user_table}.role_id = {roles_table}.id WHERE {role_user_table}.user_id = {user_id}".format(
            roles_table=self._tables['prefix'] + self._tables['roles_table'],
            role_user_table=self._tables['prefix'] + self._tables['role_user_table'],
            user_id=user_id
        )
        query_2="SELECT {permissions_table}.* FROM {permissions_table} JOIN {permission_user_table} ON {permission_user_table}.permission_id = {permissions_table}.id WHERE {permission_user_table}.user_id = {user_id}".format(
            permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
            permission_user_table=self._tables['prefix'] + self._tables['permission_user_table'],
            user_id=user_id
        )

        if roles_ids != '':
            query_3="SELECT {permissions_table}.* FROM {permissions_table} JOIN {permission_role_table} ON {permission_role_table}.permission_id = {permissions_table}.id WHERE {permission_role_table}.role_id IN ({roles_ids})".format(
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_role_table=self._tables['prefix'] + self._tables['permission_role_table'],
                roles_ids=roles_ids
            )

    def get_role(self, role_name, role_id=False):
        if role_id != False:
            query="SELECT * FROM {roles_table} WHERE id={role_id}".format(
                roles_table=self._tables['prefix'] + self._tables['roles_table'],
                role_id=role_id
            )
        elif role_name != False:
            query="SELECT * FROM {roles_table} WHERE name={role_name}".format(
                roles_table=self._tables['prefix'] + self._tables['roles_table'],
                role_name=role_name
            )
        else:
            raise PyHuskyError("Error! Invalid Method Parameters Submitted 'PyHusky_Model:get_role'")

    def get_roles(self):
        query="SELECT * FROM {roles_table}".format(
            roles_table=self._tables['prefix'] + self._tables['roles_table']
        )

    def get_permission(self, permission_name, permission_id=False):
        if permission_id != False:
            query="SELECT * FROM {permissions_table} WHERE id={permission_id}".format(
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_id=permission_id
            )
        elif permission_name != False:
            query="SELECT * FROM {permissions_table} WHERE name={permission_name}".format(
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_name=permission_name
            )
        else:
            raise PyHuskyError("Error! Invalid Method Parameters Submitted 'PyHusky_Model:get_permission'")

    def get_permissions(self):
        query="SELECT * FROM {permissions_table}".format(
            permissions_table=self._tables['prefix'] + self._tables['permissions_table']
        )

    def add_role(self, role):

        role_data={}

        if 'name' in role:
            raise PyHuskyError("Error! Role name is required 'PyHusky_Model:add_role'")
            role_data['name'] = role['name']
        else:
            role_data['name'] = role['name']

        if 'display_name' in role:
            role_data['display_name'] = role['display_name']
        else:
            role_data['display_name'] = ''

        if 'description' in role:
            role_data['description'] = role['description']
        else:
            role_data['description'] = ''

        if 'created_at' in role:
            role_data['created_at'] = role['created_at']
        else:
            role_data['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if 'updated_at' in role:
            role_data['updated_at'] = role['updated_at']
        else:
            role_data['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if 'enabled' in role:
            role_data['enabled'] = role['enabled']
        else:
            role_data['enabled'] = 1

        query="INSERT INTO {roles_table} (name, display_name, description, created_at, updated_at, enabled) VALUES ('{name}', '{display_name}', '{description}', '{created_at}', '{updated_at}', '{enabled}')".format(
            roles_table=self._tables['prefix'] + self._tables['roles_table'],
            name=role_data['name'],
            display_name=role_data['display_name'],
            description=role_data['description'],
            created_at=role_data['created_at'],
            updated_at=role_data['updated_at'],
            enabled=role_data['enabled']
        )

    def add_roles(self, roles):

        query="INSERT INTO {roles_table} (name, display_name, description, created_at, updated_at, enabled) VALUES ".format(
            roles_table=self._tables['prefix'] + self._tables['roles_table']
        )

        for role in roles:

            role_data={}

            if 'name' in role:
                raise PyHuskyError("Error! Roles name is required 'PyHusky_Model:add_roles'")
                role_data['name'] = role['name']
            else:
                role_data['name'] = role['name']

            if 'display_name' in role:
                role_data['display_name'] = role['display_name']
            else:
                role_data['display_name'] = ''

            if 'description' in role:
                role_data['description'] = role['description']
            else:
                role_data['description'] = ''

            if 'created_at' in role:
                role_data['created_at'] = role['created_at']
            else:
                role_data['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if 'updated_at' in role:
                role_data['updated_at'] = role['updated_at']
            else:
                role_data['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if 'enabled' in role:
                role_data['enabled'] = role['enabled']
            else:
                role_data['enabled'] = 1

            query += "('{name}', '{display_name}', '{description}', '{created_at}', '{updated_at}', '{enabled}'),".format(
                name=role_data['name'],
                display_name=role_data['display_name'],
                description=role_data['description'],
                created_at=role_data['created_at'],
                updated_at=role_data['updated_at'],
                enabled=role_data['enabled']
            )


    def add_permission(self, permission):
        permission_data={}

        if 'name' in permission:
            raise PyHuskyError("Error! Permission name is required 'PyHusky_Model:add_permission'")
            permission_data['name'] = permission['name']
        else:
            permission_data['name'] = permission['name']

        if 'display_name' in permission:
            permission_data['display_name'] = permission['display_name']
        else:
            permission_data['display_name'] = ''

        if 'description' in permission:
            permission_data['description'] = permission['description']
        else:
            permission_data['description'] = ''

        if 'created_at' in permission:
            permission_data['created_at'] = permission['created_at']
        else:
            permission_data['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if 'updated_at' in permission:
            permission_data['updated_at'] = permission['updated_at']
        else:
            permission_data['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if 'enabled' in permission:
            permission_data['enabled'] = permission['enabled']
        else:
            permission_data['enabled'] = 1

        query="INSERT INTO {permissions_table} (name, display_name, description, created_at, updated_at, enabled) VALUES ('{name}', '{display_name}', '{description}', '{created_at}', '{updated_at}', '{enabled}')".format(
            permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
            name=permission_data['name'],
            display_name=permission_data['display_name'],
            description=permission_data['description'],
            created_at=permission_data['created_at'],
            updated_at=permission_data['updated_at'],
            enabled=permission_data['enabled']
        )

    def add_permissions(self, permissions):
        query="INSERT INTO {permissions_table} (name, display_name, description, created_at, updated_at, enabled) VALUES ".format(
            permissions_table=self._tables['prefix'] + self._tables['permissions_table']
        )

        for permission in permissions:

            permission_data={}

            if 'name' in permission:
                raise PyHuskyError("Error! Roles name is required 'PyHusky_Model:add_permissions'")
                permission_data['name'] = permission['name']
            else:
                permission_data['name'] = permission['name']

            if 'display_name' in permission:
                permission_data['display_name'] = permission['display_name']
            else:
                permission_data['display_name'] = ''

            if 'description' in permission:
                permission_data['description'] = permission['description']
            else:
                permission_data['description'] = ''

            if 'created_at' in permission:
                permission_data['created_at'] = permission['created_at']
            else:
                permission_data['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if 'updated_at' in permission:
                permission_data['updated_at'] = permission['updated_at']
            else:
                permission_data['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if 'enabled' in permission:
                permission_data['enabled'] = permission['enabled']
            else:
                permission_data['enabled'] = 1

            query += "('{name}', '{display_name}', '{description}', '{created_at}', '{updated_at}', '{enabled}'),".format(
                name=permission_data['name'],
                display_name=permission_data['display_name'],
                description=permission_data['description'],
                created_at=permission_data['created_at'],
                updated_at=permission_data['updated_at'],
                enabled=permission_data['enabled']
            )

    def update_role(self, role, where):
        pass

    def update_permission(self, role, where):
        pass

    def update_user_roles(self, user_id, roles_data):
        pass

    def update_user_permissions(self, user_id, permissions_data):
        pass

    def remove_user_role(self, user_id, role_name, role_id=False):
        """Remove a User Role

            Args:
                user_id: User ID
                role_name: Role Name
                role_id: Role ID
        """
        if role_name != False:
            query_1="SELECT * FROM {roles_table} WHERE name={role_name}".format(
                roles_table=self._tables['prefix'] + self._tables['roles_table'],
                role_name=role_name
            )
            query_2="DELETE FROM {role_user_table} WHERE role_id={role_id} AND user_id={user_id}".format(
                role_user_table=self._tables['prefix'] + self._tables['role_user_table'],
                role_id=role_id,
                user_id=user_id
            )
        elif role_id != False:
            query="DELETE FROM {permission_user_table} WHERE permission_id={permission_id} AND user_id={user_id}".format(
                permission_user_table=self._tables['prefix'] + self._tables['permission_user_table'],
                permission_id=permission_id,
                user_id=user_id
            )
        else:
            raise PyHuskyError("Error! Role Name or Role ID Required 'PyHusky_Model:remove_user_role'")


    def remove_user_permission(self, user_id, permission_name, permission_id=False):
        """Remove a User Permission

            Args:
                user_id: User ID
                permission_name: Permission Name
                permission_id: Permission ID
        """
        if permission_name != False:
            query_1="SELECT * FROM {permissions_table} WHERE name={permission_name}".format(
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_name=permission_name
            )
            query_2="DELETE FROM {permission_user_table} WHERE permission_id={permission_id} AND user_id={user_id}".format(
                permission_user_table=self._tables['prefix'] + self._tables['permission_user_table'],
                permission_id=permission_id,
                user_id=user_id
            )
        elif permission_id != False:
            query="DELETE FROM {permission_user_table} WHERE permission_id={permission_id} AND user_id={user_id}".format(
                permission_user_table=self._tables['prefix'] + self._tables['permission_user_table'],
                permission_id=permission_id,
                user_id=user_id
            )
        else:
            raise PyHuskyError("Error! Role Name or Role ID Required 'PyHusky_Model:remove_user_permission'")


    def delete_role(self, role_name, role_id=False):
        """Delete a Role

            Args:
                role_name: Role Name
                role_id: Role ID
        """
        if role_id != False:
            query="DELETE FROM {roles_table} WHERE id={role_id}".format(
                roles_table=self._tables['prefix'] + self._tables['roles_table'],
                role_id=role_id
            )
        elif role_name != False:
            query="DELETE FROM {roles_table} WHERE name={role_name}".format(
                roles_table=self._tables['prefix'] + self._tables['roles_table'],
                role_name=role_name
            )
        else:
            raise PyHuskyError("Error! Invalid Method Parameters Submitted 'PyHusky_Model:delete_role'")

    def delete_permission(self, permission_name, permission_id=False):
        """Delete a Permission

            Args:
                permission_name: Permission Name
                permission_id: Permission ID
        """
        if permission_id != False:
            query="DELETE FROM {permissions_table} WHERE id={permission_id}".format(
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_id=permission_id
            )
        elif permission_name != False:
            query="DELETE FROM {permissions_table} WHERE name={permission_name}".format(
                permissions_table=self._tables['prefix'] + self._tables['permissions_table'],
                permission_name=permission_name
            )
        else:
            raise PyHuskyError("Error! Invalid Method Parameters Submitted 'PyHusky_Model:delete_permission'")

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
            raise PyHuskyError("Error! Cann't Connect to Database '%s'" % self._db['database'])


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