import discord
from discord.ext import commands
from discord.utils import get

import logging

logger = logging.getLogger("blitzcrank")


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logger.debug("new on_member_join {member.name}")
        channel = await member.create_dm()
        await channel.send(
            f"Hi {member.name}, please head to #rules and type !agree to become a member."
        )

    @commands.command(name="agree")
    async def agree(self, ctx: commands.Context) -> None:
        member = ctx.message.author
        logger.debug(f"new !agree {member.name}")
        role = get(member.guild.roles, name="Member")
        await member.add_roles(role, reason="user accepted rules")