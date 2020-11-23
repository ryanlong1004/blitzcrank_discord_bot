import discord
from discord.ext import commands
from discord.utils import get

from blitzcrank.cogs.permissions import Permissions

import logging

logger = logging.getLogger(__name__)


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logger.debug(f"new on_member_join {member.nick()}")
        await member.send(
            f"Hi {member.nick()}, please head to #rules and type !agree to become a member."
        )