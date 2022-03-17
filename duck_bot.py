from discord.ext import commands

from utils.permission_manager import PermissionManager
from utils.reaction_roles_data_manager import ReactionRolesDataManager
from utils.starboard_manager import StarboardManager


class DuckBot(commands.Bot):

    def __init__(self, *args, **kwargs):

        # Remove all custom added kwargs
        self.bot_config = kwargs.pop("bot_config")
        self.available_cogs = kwargs.pop("available_cogs")

        # Calls the super method to create bot instance
        super().__init__(*args, **kwargs)

        ReactionRolesDataManager.create_instance()
        PermissionManager(self.bot_config.get("Permissions"))
        StarboardManager(self.bot_config.get("Starboard"))
        self.load_cogs()

    def load_cogs(self):
        """
        Loads all the available cogs
        """
        for cog in self.available_cogs:
            self.load_extension(cog)
