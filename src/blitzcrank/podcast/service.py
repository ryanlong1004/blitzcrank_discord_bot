import datetime
import logging
import re
import typing

from blitzcrank.database.database import Database
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from .podcast import Podcast
from .rss import fetch_feed_results
from .server import publish_podcast

logger: logging.Logger = logging.getLogger(__name__)


class Service(Database):
    """Podcast Service"""

    def __init__(
        self,
        session: typing.Union[Session, None] = None,
        engine: typing.Union[Engine, None] = None,
        base: typing.Union[typing.Any, None] = None,
    ):
        """Initizalize service.  Vars are for testing.

        Args:
            session (Session, None): Session object. Defaults to None.
            engine (Engine, None): Engine object. Defaults to None.
            base (Base, None): Base object. Defaults to None.
        """
        super().__init__(session, engine, base)

    def save(self, podcast: Podcast) -> Podcast:
        """Saves a podcast to persistence

        Args:
            podcast (Podcast): object
        """
        logger.debug(f"saving {self.__class__} {podcast}")
        super().get_base().metadata.create_all(super().get_engine())
        super().get_session().add(podcast)
        super().get_session().commit()
        return self.fetch_last_local()

    def fetch_last_local(self) -> Podcast:
        """Returns the last podcast collected from remote by created
        date in descending order.

        Returns:
            Podcast: object
        """
        logger.debug(f"fetching last local {self.__class__}")
        return (
            super().get_session().query(Podcast).order_by(Podcast.created_at.desc())[0]
        )

    @staticmethod
    def publish(podcast: Podcast, url: str):
        """Publishes podcast to url

        Args:
            podcast (Podcast): object
            url (str): webhook url to publish to
        """
        logger.debug(f"publishing {podcast}")
        publish_podcast(podcast, url)

    def fetch_last_remote(self) -> Podcast:
        """Returns the last remote podcast from the RSS feed based
        on the first value returned.

        Returns:
            Podcast: object
        """
        logging.debug(f"fetching last remote {self.__class__}")
        return Podcast(
            **_from_results(
                fetch_feed_results("https://www.codingblocks.net/feed/podcast")
            )
        )


def _from_results(results) -> typing.Dict:
    """Returns a dictionary for Coding Blocks Podcast

    Args:
        results (FeedParserDict): feedparser results from rss feed

    Returns:
        typing.Dict: parsed dictionary

    TODO: DRY up for other podcasts
    """
    IMAGE_URL_PATTERN = r"(src=\")(\S*)(\")"

    if len(results) < 1:
        return {}

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


if __name__ == "__main__":
    pass
