import logging
from typing import Union

from blitzcrank.services import MemberRoleException, grant_member_role
from discord.ext import commands
from discord.utils import get

logger = logging.getLogger(__name__)


class Permissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = member.guild.system_channel
    #     if channel is not None:
    #         await channel.send('Welcome {0.mention}.'.format(member))

    # @commands.command()
    # async def hello(self, ctx, *, member: discord.Member = None):
    #     """Says hello"""
    #     member = member or ctx.author
    #     if self._last_member is None or self._last_member.id != member.id:
    #         await ctx.send('Hello {0.name}~'.format(member))
    #     else:
    #         await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
    #     self._last_member = member

    @commands.command()
    async def mentor(self, ctx: commands.Context) -> None:
        try:
            await grant_member_role(ctx, "Mentor")
            await ctx.message.author.send(f"Mentor role granted")
        except MemberRoleException as e:
            logger.error(e)
            await ctx.message.author.send(
                f"Unable to grant role.  Admin has been notified."
            )

    @commands.command(name="agree")
    async def member(self, ctx: commands.Context) -> None:
        try:
            await grant_member_role(ctx, "Member")
            await ctx.message.author.send(f"Member role granted")
        except Exception as e:
            logger.error(e)
            await ctx.message.author.send(
                f"Unable to grant role.  Admin has been notified."
            )
