import discord
from discord.ext import commands
from discord.utils import get

from utils.reaction_roles_data_manager import ReactionRolesDataManager
from utils.starboard_manager import StarboardManager


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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        Called whenever a reaction is added in a guild. Handles starboard reactions
        """

        if payload.member.id == self.client.user.id:
            return

        if payload.emoji.name == StarboardManager.get_instance().emoji:

            if payload.message_id not in StarboardManager.get_instance().messages:

                channel = self.client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                reaction = get(message.reactions, emoji=payload.emoji.name)

                if reaction.count >= StarboardManager.get_instance().reaction_threshold:
                    starboard_channel = self.client.get_channel(StarboardManager.get_instance().channel_id)

                    embed = discord.Embed(description=message.content, color=10692152)
                    embed.set_footer(text=f"By {message.author}")

                    StarboardManager.get_instance().add_message(payload.message_id)
                    await starboard_channel.send(embed=embed)


def setup(client):
    client.add_cog(ReactionEvent(client))
