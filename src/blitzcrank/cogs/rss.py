import feedparser
import re
from discord import Embed, Webhook, RequestsWebhookAdapter


class Podcast(dict):
    PATTERN = r"(src=\")(\S*)(\")"

    def __repr__(self):
        return f"{self.__dict__.items()}"

    @classmethod
    def from_feed(cls, url):
        results = feedparser.parse(url)
        return Podcast(
            {
                "id": results["entries"][0]["id"],
                "url": results["entries"][0]["link"],
                "description": results["entries"][0]["subtitle"],
                "title": f"{results['entries'][0]['itunes_title']} ({results['entries'][0]['itunes_episode']})",
                "type": "rich",
                "image": {
                    "url": re.search(
                        cls.PATTERN, results["entries"][0]["summary"]
                    ).group(2),
                },
            }
        )


def publish(podcast: "Podcast"):
    embeded = Embed.from_dict(podcast)
    webhook = Webhook.from_url(
        "https://discord.com/api/webhooks/793195455194333186/Kvie1rOoBa28XyKb15epsnZmQ0EIQ16GnSonJ8Gfi1K4Wpn907mIcRpjRlhM6fCAKPrh",
        adapter=RequestsWebhookAdapter(),
    )
    webhook.send(embed=embeded)
    print(embeded)


if __name__ == "__main__":
    p = Podcast.from_feed("https://www.codingblocks.net/feed/podcast")
    publish(p)