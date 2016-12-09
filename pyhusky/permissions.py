# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""


class Permissions(object):
    """Permissions Module"""

    def add_permissions(self, permissions):
        """ Add Many Permissions

            Args:
                permissions: A list of all permissions data for example
                    [
                        { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc", "users_ids": (1, 2, 3, 58, 56) },
                        { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc", "users_ids": (1, 2, 3, 58, 56) },
                        { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc", "users_ids": (1, 2, 3, 58, 56) },
                        ....
                    ]
                    Only permission name is required

            Returns:
                True if successful, False otherwise.

        """
        pass

    def add_permission(self, permission):
        """ Add a New Permission

            Args:
                role: A dict of role data for example
                    { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc", "users_ids": (1, 2, 3, 58, 56) }
                    Only permission name is required

            Returns:
                True if successful, False otherwise.

        """
        pass

    def has_permission(self, user_id, permission_name):
        pass

    def get_permission(self, **options):
        pass

    def update_permission(self, permission_name=False, permission_id=False, **new_data):
        pass

    def delete_permission(self, **options):
        pass