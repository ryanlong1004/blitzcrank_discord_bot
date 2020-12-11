import logging

import discord
from discord.ext import commands
from discord.utils import get

logger = logging.getLogger(__name__)


class AdminUtilities(commands.Cog):
    def __init__(self, bot, CLIENT_ID):
        self.bot = bot
        self.client_id = CLIENT_ID

    @commands.command(name="oauth2")
    @commands.has_role("Admin")
    async def oauth2_url(self, ctx: commands.Context) -> None:
        """Sends the oauth2 url for the bot to the chat room

        Args:
            ctx (commands.Context): context
        """
        logger.debug("sending Oauth2 url")
        await ctx.message.author.send(discord.utils.oauth_url(self.client_id))
