import logging
import feedparser
import re

from blitzcrank.services.discordx import publish
from discord.ext import commands, tasks


logger = logging.getLogger(__name__)


class Podcast(dict):
    """Represents podcast data """

    def __repr__(self):
        return f"{self.__dict__.items()}"

    @classmethod
    def fetch_feed(cls, url):
        """Returns data from RSS feed

        Args:
            url (str): URL to fetch RSS data from

        Returns:
            FeedParserDict: data fetched
        """
        try:
            return feedparser.parse(url)
        except Exception as e:
            logger.error(str(e))


class CodingBlocks(Podcast):
    """Represents CodingBlocks podcast data """

    IMAGE_URL_PATTERN = r"(src=\")(\S*)(\")"

    @classmethod
    def id(cls, results):
        return results["entries"][0]["id"]

    @classmethod
    def description(cls, results):
        return results["entries"][0]["subtitle"]

    @classmethod
    def url(cls, results):
        return results["entries"][0]["link"]

    @classmethod
    def title(cls, results):
        return f"{results['entries'][0]['itunes_title']} ({results['entries'][0]['itunes_episode']})"

    @classmethod
    def image(cls, results):
        url: str = re.search(
            cls.IMAGE_URL_PATTERN, results["entries"][0]["summary"]
        ).group(2)
        if url is None or url is "":
            raise AttributeError("could not locate image url")
        return {
            "url": url,
        }

    @classmethod
    def from_feed(cls, url) -> Podcast:
        """Returns Podcast object from feed

        Args:
            url ([type]): [description]

        Returns:
            Podcast: [description]
        """
        try:
            results = super().fetch_feed(url)
        except Exception as e:
            logger.error(e)
            return Podcast()

        return Podcast(
            {
                "id": cls.id(results),
                "url": cls.url(results),
                "description": cls.description(results),
                "title": cls.title(results),
                "type": "rich",
                "image": cls.image(results),
            }
        )


class RSS(commands.Cog):
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
        podcast = CodingBlocks.from_feed("https://www.codingblocks.net/feed/podcast")
        publish(
            podcast,
            "https://discord.com/api/webhooks/793195455194333186/Kvie1rOoBa28XyKb15epsnZmQ0EIQ16GnSonJ8Gfi1K4Wpn907mIcRpjRlhM6fCAKPrh",
        )

    @update.before_loop
    async def before_update(self) -> None:
        await self.bot.wait_until_ready()


if __name__ == "__main__":
    pass
