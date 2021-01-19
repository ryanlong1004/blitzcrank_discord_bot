import datetime
import logging
import feedparser
import re

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.engine.base import Engine

from blitzcrank.services.discordx import publish
from discord.ext import commands, tasks

from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
engine: Engine = create_engine(f"sqlite:///test.db")
Session.configure(bind=engine)
session = Session()


class Podcast(Base):
    """Represents podcast data """

    __tablename__ = "podcast"

    id = Column(String, primary_key=True)
    description = Column(String)
    url = Column(String)
    title = Column(String)
    image = Column(String)
    type = Column(String)
    created_at = Column("created_at", DateTime, nullable=False)

    def as_embed(self):
        return {
            "id": self.id,
            "description": self.description,
            "url": self.url,
            "title": self.title,
            "image": {
                "url": self.image,
            },
        }


def from_results(results):
    IMAGE_URL_PATTERN = r"(src=\")(\S*)(\")"

    return {
        "id": results["entries"][0]["id"],
        "description": results["entries"][0]["subtitle"],
        "url": results["entries"][0]["link"],
        "title": f"{results['entries'][0]['itunes_title']} ({results['entries'][0]['itunes_episode']})",
        "image": re.search(IMAGE_URL_PATTERN, results["entries"][0]["summary"]).group(
            2
        ),
        "type": "rich",
        "created_at": datetime.datetime.utcnow(),
    }


class CodingBlocks:
    """Represents CodingBlocks podcast data """

    @classmethod
    def from_feed(cls, url) -> Podcast:
        """Returns Podcast object from feed

        Args:
            url ([type]): [description]

        Returns:
            Podcast: [description]
        """
        try:
            results = feedparser.parse(url)
        except Exception as e:
            logger.error(e)
            return Podcast()

        try:
            data = from_results(results)
            podcast = Podcast(**data)
            return podcast
        except Exception as e:
            print(f"Unable to process podcast feed: {e}")
            logger.warning(f"Unable to process podcast feed: {e}")
            return Podcast()


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
        last = session.query(Podcast).order_by("created_at")[0]
        if podcast.id != last.id:
            try:
                publish(
                    podcast.as_embed(),
                    "https://discord.com/api/webhooks/793195455194333186/Kvie1rOoBa28XyKb15epsnZmQ0EIQ16GnSonJ8Gfi1K4Wpn907mIcRpjRlhM6fCAKPrh",
                )
                Base.metadata.create_all(engine)
                session.add(podcast)
                session.commit()
            except Exception as e:
                logger.warning(f"Publish podcast failed: {e} - {podcast}")
                self.update.stop()

    @update.before_loop
    async def before_update(self) -> None:
        await self.bot.wait_until_ready()


if __name__ == "__main__":
    pass
