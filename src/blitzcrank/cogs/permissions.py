import discord
from discord.ext import commands
from discord.utils import get

import logging

logger = logging.getLogger("blitzcrank")


class Permissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # @commands.has_role("Admin")
    # async def kisses(self, ctx: commands.Context) -> None:
    #     response = "Muah muah muah"
    #     await ctx.send(response)

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

    @commands.command(name="mentor")
    async def mentor(self, ctx: commands.Context) -> None:
        member = ctx.message.author
        role = get(member.guild.roles, name="Mentor")
        logger.info(f"Granting 'Mentor' role to {member.name}")
        await member.add_roles(role, reason="user requested")
