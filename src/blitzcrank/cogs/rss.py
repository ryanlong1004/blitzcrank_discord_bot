import feedparser
import re
from discord import Embed


class Podcast:
    PATTERN = r"(src=\")(\S*)(\")"

    def __init__(self, id, link, image):
        self.id = id
        self.ink = link
        self.image = image

    def __repr__(self):
        return f"{self.__dict__.items()}"

    def __get__(self, instance, owner):
        pass

    @classmethod
    def from_feed(cls, url):
        results = feedparser.parse(url)
        id = results["entries"][0]["id"]
        link = results["entries"][0]["link"]
        image = re.search(cls.PATTERN, results["entries"][0]["summary"]).group(2)
        return Podcast(id, link, image)


def publish(podcast: "Podcast"):
    embeded = Embed.from_dict(podcast)
    print(embeded)


if __name__ == "__main__":
    p = Podcast.from_feed("https://www.codingblocks.net/feed/podcast")
    publish(p)