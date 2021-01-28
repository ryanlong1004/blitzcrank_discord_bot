import logging

import discord
from discord.ext import commands
from discord.utils import get

logger: logging.Logger = logging.getLogger(__name__)


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logger.debug(f"new on_member_join {member.nick()}")
        await member.send(f"Hi {member.nick()}, welcome to the rlong.io server.")
