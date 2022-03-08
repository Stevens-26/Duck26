from discord.ext import commands
from discord.utils import get

from utils.reaction_roles_data_manager import ReactionRolesDataManager


class ReactionEvent(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.reaction_roles_data_manager = ReactionRolesDataManager.get_instance()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """ Called whenever a reaction is added in a guild. """

        if payload.member.id == self.client.user.id:
            return

        if payload.message_id in ReactionRolesDataManager.get_instance().reaction_messages:
            role_id = ReactionRolesDataManager.get_instance().get_role_id(payload.message_id, payload.emoji.name)

            if role_id is None:
                return

            role = get(payload.member.guild.roles, id=role_id)

            if role not in payload.member.roles:
                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """ Called whenever a reaction is removed in a guild. """

        if payload.user_id == self.client.user.id:
            return

        if payload.message_id in ReactionRolesDataManager.get_instance().reaction_messages:

            role_id = ReactionRolesDataManager.get_instance().get_role_id(payload.message_id, payload.emoji.name)

            # Checks to ensure the reaction role exists
            if role_id is not None:

                guild = self.client.get_guild(payload.guild_id)
                member = get(guild.members, id=payload.user_id)
                role = get(guild.roles, id=role_id)

                if role in member.roles:
                    await member.remove_roles(role)


def setup(client):
    client.add_cog(ReactionEvent(client))
