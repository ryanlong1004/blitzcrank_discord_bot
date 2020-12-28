import logging
import feedparser
import re
from discord import Embed, Webhook, RequestsWebhookAdapter
from feedparser.util import FeedParserDict

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
        return feedparser.parse(url)

    def publish(self, url):
        """Publishes podcast to Discord as embed

        Args:
            podcast (Podcast): podcast to publish
            webhook_url (str): Discord webhook URL
        """

        embeded = Embed.from_dict(self)
        webhook = Webhook.from_url(
            url,
            adapter=RequestsWebhookAdapter(),
        )
        webhook.send(embed=embeded)


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
        return {
            "url": re.search(
                cls.IMAGE_URL_PATTERN, results["entries"][0]["summary"]
            ).group(2),
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


if __name__ == "__main__":
    podcast = CodingBlocks.from_feed(
        "https://www.codingblocks.net/feed/podcast"
    ).publish(
        "https://discord.com/api/webhooks/793195455194333186/Kvie1rOoBa28XyKb15epsnZmQ0EIQ16GnSonJ8Gfi1K4Wpn907mIcRpjRlhM6fCAKPrh"
    )
