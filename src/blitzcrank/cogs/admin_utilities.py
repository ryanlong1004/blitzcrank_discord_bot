import discord
from discord.ext import commands
from discord.utils import get

import logging

logger = logging.getLogger("blitzcrank")


class AdminUtilities(commands.Cog):
    def __init__(self, bot, CLIENT_ID):
        self.bot = bot
        self.client_id = CLIENT_ID

    @commands.command(name="oauth2")
    @commands.has_role("Admin")
    async def oauth2_url(self, ctx: commands.Context) -> str:
        logger.info("sending Oauth2 url")
        await ctx.send(discord.utils.oauth_url(self.client_id))