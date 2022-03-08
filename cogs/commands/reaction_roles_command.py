import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from utils.permission_manager import PermissionManager
from utils.reaction_roles_data_manager import ReactionRolesDataManager


class ReactionRoleCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def clean_emoji_name(emoji):
        if "<:" in emoji:
            emoji = emoji[2:]
            return emoji[:emoji.index(":")]
        return emoji

    @commands.group(name="rr")
    async def reaction_role(self, ctx):
        """ The base group command for reaction roles. """
        if ctx.invoked_subcommand is None:
            await ctx.send("Please use one of the subcommands! ``add, remove, clear, list``")

    @reaction_role.group()
    async def add(self, ctx, message_id, _emoji_name, role: discord.Role):
        """ Adds the given message and emoji as a reaction role. """
        if PermissionManager.get_instance().check_member_permission(ctx.author):

            emoji_name = self.clean_emoji_name(_emoji_name)
            msg = await ctx.fetch_message(int(message_id))
            ReactionRolesDataManager.get_instance().add_reaction_role(message_id, emoji_name, role.id)

            try:
                await msg.add_reaction(_emoji_name)
            except Exception as e:
                if "Unknown Emoji" in str(e):
                    await ctx.send(
                        "**ERROR**: Unable to add reaction! The reaction-role will work once the emoji is manually "
                        "added!")

            await ctx.send("Reaction role Added!")

    @add.error
    async def add_reaction_role_error(self, ctx, error):
        """ Handles any errors in add command. """
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Missing required arguments ``<message_id> <emoji_name> <role>``")

        else:
            await ctx.send("There was an error adding the reaction role!")
            print(error)

    @reaction_role.group()
    async def remove(self, ctx, message_id, emoji_name):
        """ Removes the given reaction role """
        if PermissionManager.get_instance().check_member_permission(ctx.author):
            ReactionRolesDataManager.get_instance().remove_reaction_role(message_id, emoji_name)
            await ctx.send("Reaction role removed!")

    @remove.error
    async def remove_error(self, ctx, error):
        """ Handles any errors in remove command """
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Missing required arguments ``<message_id> <emoji_name>``")

        else:
            await ctx.send("There was an error removing the reaction role!")

    @reaction_role.group()
    async def clear(self, ctx, message_id):
        """ Clears all reaction roles for the given message id. """

        if PermissionManager.get_instance().check_member_permission(ctx.author):
            ReactionRolesDataManager.get_instance().clear_reaction_roles(message_id)
            await ctx.send("Reaction roles cleared for given message!")

    @clear.error
    async def clear_error(self, ctx, error):
        """ Handles any errors in clear subcommand. """

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Missing required arguments ``<message_id>``")

        else:
            await ctx.send("There was an error clearing the reaction roles!")

    @reaction_role.group()
    async def list(self, ctx, message_id):
        """ Lists all reaction roles for the given message id. """

        if PermissionManager.get_instance().check_member_permission(ctx.author):

            if int(message_id) not in ReactionRolesDataManager.get_instance().reaction_roles.keys():
                await ctx.send("No reactions roles exist for the given message!")
                return

            embed = discord.Embed(colour=0xa32638)
            reaction_roles = ReactionRolesDataManager.get_instance().reaction_roles[int(message_id)]
            description = f"**Reaction Roles for {message_id}** \n \n"

            # Iterates over all reaction roles for the given message, adds each to the embed
            for reaction_role in reaction_roles:
                description += f"""{reaction_role} <@&{ReactionRolesDataManager.get_instance().get_role_id(
                    int(message_id), reaction_role)}>\n"""

            embed.description = description

            await ctx.send(embed=embed)

    @list.error
    async def list_error(self, ctx, error):
        """ Handles any errors in list subcommand. """

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Missing required arguments ``<message_id>``")
        else:
            print(error)
            await ctx.send("There was an error listing the reaction roles!")


def setup(client):
    client.add_cog(ReactionRoleCommand(client))
