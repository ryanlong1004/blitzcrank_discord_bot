import logging

from blitzcrank.podcast.service import Service
from discord.ext import commands, tasks

logger: logging.Logger = logging.getLogger(__name__)

service: Service = Service()


class Podcasts(commands.Cog):
    """Cog for getting the latest videos from Youtube channels and sending
    them to their channel via webhook

    Args:
        commands (commands.Cog): Cog base class
    """

    def __init__(self, bot):
        self.bot = bot
        self.webhook_url = "https://discord.com/api/webhooks/793195455194333186/Kvie1rOoBa28XyKb15epsnZmQ0EIQ16GnSonJ8Gfi1K4Wpn907mIcRpjRlhM6fCAKPrh"
        self.update.start()

    @tasks.loop(seconds=60 * 30)
    async def update(self) -> None:
        logger.debug(f"checking for podcast updates")
        service.run_tasks()

    @update.before_loop
    async def before_update(self) -> None:
        logger.debug("Waiting for bot to initialize")
        await self.bot.wait_until_ready()
