import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, Iterator, List, Tuple

import requests
from blitzcrank.youtube.service import Service
from discord.ext import commands, tasks
from discord_webhook.webhook import DiscordEmbed, DiscordWebhook

logger: logging.Logger = logging.getLogger(__name__)


class LimitExceededWarning(Exception):
    """Exception raised for errors in the input."""

    pass


class YouTube(commands.Cog):
    """Cog for getting the latest videos from Youtube channels and sending
    them to their channel via webhook

    Args:
        commands (commands.Cog): Cog base class
    """

    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    @tasks.loop(seconds=60 * 60)
    async def update(self):
        logger.debug("checking for Youtube updates")
        service = Service()
        service.run_tasks()

    @update.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()