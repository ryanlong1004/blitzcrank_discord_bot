import logging

import discord
from discord.ext import commands
from discord.utils import get

logger: logging.Logger = logging.getLogger(__name__)


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kisses(self, ctx: commands.Context) -> None:
        logger.debug("Kisses called")
        response = "Muah muah muah"
        await ctx.send(response)

    # @commands.command()
    # async def hello(self, ctx: commands.Context, *, member: discord.Member = None):
    #     """Says hello"""
    #     logger.debug("Say hello called.")
    #     member = member or ctx.author
    #     if self._last_member is None or self._last_member.id != member.id:
    #         await ctx.send("Hello {0.name}~".format(member))
    #     else:
    #         await ctx.send("Hello {0.name}... This feels familiar.".format(member))
    #     self._last_member = member
