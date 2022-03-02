import discord


class PermissionManager:

    instance = None

    @staticmethod
    def get_instance():
        """ Gets the instance of the PermissionManager """
        return PermissionManager.instance

    def __init__(self, permission_config):
        self.permission_config = permission_config
        self.permission_roles = permission_config.get("addReactionRoles")

        # Ensures the the instance is defined
        PermissionManager.instance = self

    def check_member_permission(self, member: discord.Member):
        """
        Checks if the given member has the required role/permissions to use the commands
        :param member: A discord.Member object
        :return bool: The bool value whether the member has the required permission(s)
        """

        # Checks if the user is a guild administrator
        if member.guild_permissions.administrator:
            return True

        # Checks if the user has any of the permission required roles
        if any(role.id in self.permission_roles for role in member.roles):
            return True

        return False
