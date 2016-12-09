# -*- coding: utf-8 -*-
"""
    PyHusky
    ~~~~~~
    Python Role Based Permissions Library
    :copyright: (c) 2016 by Clivern (hello@clivern.com).
    :license: MIT, see LICENSE for more details.
"""

class Roles(object):
    """Roles Module"""


    def add_roles(self, roles):
        """ Add Many Roles

            Args:
                roles: A list of all roles data for example
                    [{
                        "name": "role_name",
                        "display_name": "Role Name",
                        "description": "Role Description...etc",
                        "permissions": [
                            { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc" },
                            { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc" },
                            { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc" },
                            ....
                        ],
                        "users_ids" => (1, 2, 3, 58, 56)
                    }]
                    Only role name is required

            Returns:
                True if successful, False otherwise.

        """
        pass

    def add_role(self, role):
        """ Add a New Role

            Args:
                role: A dict of role data for example
                    {
                        "name": "role_name",
                        "display_name": "Role Name",
                        "description": "Role Description...etc",
                        "permissions": [
                            { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc" },
                            { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc" },
                            { "name": "permission_name", "display_name": "Permission Name", "description": "Permission Description..etc" },
                            ....
                        ],
                        "users_ids" => (1, 2, 3, 58, 56)
                    }
                    Only role name is required

            Returns:
                True if successful, False otherwise.

        """
        pass

    def has_role(self, user_id, role_name):
        pass

    def get_role(self, role_name=False, role_id=False):
        pass

    def update_role(self, role_name=False, role_id=False, **new_data):
        pass

    def delete_role(self, role_name=False, role_id=False):
        pass