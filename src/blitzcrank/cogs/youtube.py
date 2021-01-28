import logging

from blitzcrank.youtube.service import Service
from discord.ext import commands, tasks

logger: logging.Logger = logging.getLogger(__name__)

service: Service = Service()


class YouTube(commands.Cog):
    """Cog for getting the latest videos from Youtube channels and sending
    them to their channel via webhook

    Args:
        commands (commands.Cog): Cog base class
    """

    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    @tasks.loop(seconds=60 * 30)
    async def update(self):
        logger.debug("checking for Youtube updates")
        service.run_tasks()

    @update.before_loop
    async def before_update(self):
        logger.debug("waiting for bot to be ready")
        await self.bot.wait_until_ready()
