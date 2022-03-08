from discord.ext import commands

from utils.permission_manager import PermissionManager


class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx) -> None:
        """ Basic ping command to test if bot is online and view current latency. """

        if PermissionManager.get_instance().check_member_permission(ctx.author):
            latency = self.client.latency * 1000
            await ctx.send(f"The ping is ``{round(latency, 3)}ms``")


def setup(client):
    client.add_cog(Ping(client))
