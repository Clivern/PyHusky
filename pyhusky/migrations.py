# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""

import pymysql.cursors
"""


# Connect to the database
connection = pymysql.connect(host=_db['host'],
                             user=_db['username'],
                             password=_db['password'],
                             db=_db['database'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
"""



class MySQLMigration(object):
    """MySQL Migration Module"""

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

    def __init__(self, db, tables):
        self._connect()

    def create_roles_table(self):
        query="""CREATE TABLE IF NOT EXISTS `{prefix}{table}` (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
              `display_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `enabled` tinyint(1) NOT NULL DEFAULT '0',
              PRIMARY KEY (`id`),
              UNIQUE KEY `roles_name_unique` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""".format(prefix=self._tables['prefix'], table=self._tables['roles_table'])
        return self._query(query)

    def create_permissions_table(self):
        query="""CREATE TABLE IF NOT EXISTS `{prefix}{table}` (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
              `display_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `enabled` tinyint(1) NOT NULL DEFAULT '0',
              PRIMARY KEY (`id`),
              UNIQUE KEY `permissions_name_unique` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""".format(prefix=self._tables['prefix'], table=self._tables['permissions_table'])
        return self._query(query)

    def create_permission_role_table(self):
        query="""CREATE TABLE IF NOT EXISTS `{prefix}{table}` (
              `permission_id` int(10) unsigned NOT NULL,
              `role_id` int(10) unsigned NOT NULL,
              PRIMARY KEY (`permission_id`,`role_id`),
              KEY `permission_role_role_id_foreign` (`role_id`),
              CONSTRAINT `permission_role_permission_id_foreign` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
              CONSTRAINT `permission_role_role_id_foreign` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""".format(prefix=self._tables['prefix'], table=self._tables['permission_role_table'])
        return self._query(query)

    def create_role_user_table(self):

        if self._tables['users_table'] != False and self._tables['users_table_id'] != False:
            users_table_constraint=""",
            CONSTRAINT `role_user_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `{users_table}` (`{users_table_id}`) ON DELETE CASCADE ON UPDATE CASCADE
            """.format(users_table=self._tables['users_table'], users_table_id=self._tables['users_table_id'])
        else:
            users_table_constraint=""

        query="""CREATE TABLE IF NOT EXISTS `{prefix}{table}` (
              `user_id` int(10) unsigned NOT NULL,
              `role_id` int(10) unsigned NOT NULL,
              PRIMARY KEY (`user_id`,`role_id`),
              KEY `role_user_role_id_foreign` (`role_id`),
              CONSTRAINT `role_user_role_id_foreign` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE{users_table_constraint}
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""".format(prefix=self._tables['prefix'], table=self._tables['role_user_table'], users_table_constraint=users_table_constraint)
        return self._query(query)

    def create_permission_user_table(self):

        if self._tables['users_table'] != False and self._tables['users_table_id'] != False:
            users_table_constraint=""",
            CONSTRAINT `permission_user_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `{users_table}` (`{users_table_id}`) ON DELETE CASCADE ON UPDATE CASCADE
            """.format(users_table=self._tables['users_table'], users_table_id=self._tables['users_table_id'])
        else:
            users_table_constraint=""

        query="""CREATE TABLE IF NOT EXISTS `{prefix}{table}` (
              `permission_id` int(10) unsigned NOT NULL,
              `user_id` int(10) unsigned NOT NULL,
              PRIMARY KEY (`permission_id`,`user_id`),
              KEY `permission_user_user_id_foreign` (`user_id`),
              CONSTRAINT `permission_user_permission_id_foreign` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
              CONSTRAINT `permission_user_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""".format(prefix=self._tables['prefix'], table=self._tables['permission_user_table'])
        return self._query(query)

    def drop_roles_table(self):
        query="DROP TABLE IF EXISTS `{prefix}{table}`;".format(prefix=self._tables['prefix'], table=self._tables['roles_table'])
        return self._query(query)

    def drop_permissions_table(self):
        query="DROP TABLE IF EXISTS `{prefix}{table}`;".format(prefix=self._tables['prefix'], table=self._tables['permissions_table'])
        return self._query(query)

    def drop_permission_role_table(self):
        query="DROP TABLE IF EXISTS `{prefix}{table}`;".format(prefix=self._tables['prefix'], table=self._tables['permission_role_table'])
        return self._query(query)

    def drop_role_user_table(self):
        query="DROP TABLE IF EXISTS `{prefix}{table}`;".format(prefix=self._tables['prefix'], table=self._tables['role_user_table'])
        return self._query(query)

    def drop_permission_user_table(self):
        query="DROP TABLE IF EXISTS `{prefix}{table}`;".format(prefix=self._tables['prefix'], table=self._tables['permission_user_table'])
        return self._query(query)

    def table_exists(self, table_name):
        with self._connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE '" + table_name +"';")
        self._connection.commit()
        for row in cursor:
            return table_name in row.values()

    def _connect(self):
        self._connection = pymysql.connect(host=self._db['host'],
                                     user=self._db['username'],
                                     password=self._db['password'],
                                     db=self._db['database'],
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def close(self):
        self._connection.close()

    def _query(self, query):
        with self._connection.cursor() as cursor:
            cursor.execute(query)
        self._connection.commit()

"""
mig = MySQLMigration({},{})
mig.create_roles_table()
print(mig.table_exists('roles_table'))
mig.drop_roles_table()
mig.close()
"""

class SQLLiteMigration(object):
    """SQLLite Migration Module"""
    pass


class PostgreSQLMigration(object):
    """PostgreSQL Migration Module"""
    pass