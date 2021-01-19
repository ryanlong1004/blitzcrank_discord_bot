import logging

from discord.ext import commands, tasks
from blitzcrank.podcast.podcast import Podcast

from blitzcrank.podcast.service import Service as PodcastService

logger = logging.getLogger(__name__)

podcast_service = PodcastService()


class Podcasts(commands.Cog):
    """Cog for getting the latest videos from Youtube channels and sending
    them to their channel via webhook

    Args:
        commands (commands.Cog): Cog base class
    """

    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    @tasks.loop(seconds=60 * 60 * 60 * 24)
    async def update(self) -> None:
        logger.debug("checking for RSS updates")
        podcast = podcast_service.fetch_recent_podcast()
        last = podcast_service.last()
        print(podcast.id)
        print(last.id)
        if podcast.id != last.id:
            try:
                podcast_service.publish(
                    podcast,
                    "https://discord.com/api/webhooks/793195455194333186/Kvie1rOoBa28XyKb15epsnZmQ0EIQ16GnSonJ8Gfi1K4Wpn907mIcRpjRlhM6fCAKPrh",
                )
                podcast_service.save(podcast)  # TODO Will need error handling
            except Exception as e:
                logger.warning(f"Publish podcast failed: {e} - {podcast}")
                self.update.stop()

    @update.before_loop
    async def before_update(self) -> None:
        await self.bot.wait_until_ready()
