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
        mig = MySQLMigration({},{})
        self.assertEqual(mig.create_roles_table(),"""CREATE TABLE `ph_roles` (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
              `display_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `enabled` tinyint(1) NOT NULL DEFAULT '0',
              PRIMARY KEY (`id`),
              UNIQUE KEY `roles_name_unique` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""")
        self.assertEqual(mig.create_roles_table(),"""CREATE TABLE `ph_roles` (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
              `display_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `enabled` tinyint(1) NOT NULL DEFAULT '0',
              PRIMARY KEY (`id`),
              UNIQUE KEY `roles_name_unique` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""")
        self.assertEqual(mig.create_permissions_table(),"""CREATE TABLE `ph_permissions` (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
              `display_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
              `enabled` tinyint(1) NOT NULL DEFAULT '0',
              PRIMARY KEY (`id`),
              UNIQUE KEY `permissions_name_unique` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""")
        self.assertEqual(mig.create_permission_role_table(),"""CREATE TABLE `ph_permission_role` (
              `permission_id` int(10) unsigned NOT NULL,
              `role_id` int(10) unsigned NOT NULL,
              PRIMARY KEY (`permission_id`,`role_id`),
              KEY `permission_role_role_id_foreign` (`role_id`),
              CONSTRAINT `permission_role_permission_id_foreign` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
              CONSTRAINT `permission_role_role_id_foreign` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""")
        self.assertEqual(mig.create_role_user_table(),"""CREATE TABLE `ph_role_user` (
              `user_id` int(10) unsigned NOT NULL,
              `role_id` int(10) unsigned NOT NULL,
              PRIMARY KEY (`user_id`,`role_id`),
              KEY `role_user_role_id_foreign` (`role_id`),
              CONSTRAINT `role_user_role_id_foreign` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""")
        self.assertEqual(mig.create_permission_user_table(),"""CREATE TABLE `ph_permission_user` (
              `permission_id` int(10) unsigned NOT NULL,
              `user_id` int(10) unsigned NOT NULL,
              PRIMARY KEY (`permission_id`,`user_id`),
              KEY `permission_user_user_id_foreign` (`user_id`),
              CONSTRAINT `permission_user_permission_id_foreign` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
              CONSTRAINT `permission_user_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""")

        self.assertEqual(mig.drop_roles_table(),"""DROP TABLE IF EXISTS `ph_roles`;""")
        self.assertEqual(mig.drop_permissions_table(),"""DROP TABLE IF EXISTS `ph_permissions`;""")
        self.assertEqual(mig.drop_permission_role_table(),"""DROP TABLE IF EXISTS `ph_permission_role`;""")
        self.assertEqual(mig.drop_role_user_table(),"""DROP TABLE IF EXISTS `ph_role_user`;""")
        self.assertEqual(mig.drop_permission_user_table(),"""DROP TABLE IF EXISTS `ph_permission_user`;""")


if __name__ == '__main__':
    unittest.main()
