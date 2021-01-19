import datetime
import logging
import re
import typing

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from .podcast import Podcast
from .rss import fetch_feed_results
from .server import publish_podcast

logger: logging.Logger = logging.getLogger(__name__)


class Service:
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
        self.session: typing.Union[Session, None] = session
        self.engine: typing.Union[Engine, None] = engine
        self.base: typing.Union[typing.Any, None] = base

    def save(self, podcast: Podcast) -> Podcast:
        """Saves a podcast to persistence

        Args:
            podcast (Podcast): object
        """
        logger.debug(f"saving {self.__class__} {podcast}")
        self._get_base().metadata.create_all(self._get_engine())
        self._get_session().add(podcast)
        self._get_session().commit()
        return self.fetch_last_local()

    def fetch_last_local(self) -> Podcast:
        """Returns the last podcast collected from remote by created
        date in descending order.

        Returns:
            Podcast: object
        """
        logger.debug(f"fetching last local {self.__class__}")
        return self._get_session().query(Podcast).order_by(Podcast.created_at.desc())[0]

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

    def _get_session(self) -> typing.Union[Session, None]:
        """Creates new session if none exist.

        Returns:
            typing.Union[Session, None]: returns Session
        """
        if self.session is None:
            Session = sessionmaker()
            Session.configure(bind=self._get_engine())
            self.session = Session()
        return self.session

    def _get_engine(self) -> typing.Union[Engine, None]:
        """Creates a new engine if none exist.

        Returns:
            typing.Union[Engine, None]: returns Engine
        """
        if self.engine is None:
            self.engine = create_engine(f"sqlite:///test.db")
        return self.engine

    def _get_base(self) -> typing.Union[typing.Any, None]:
        """Creates a new base if none exist.

        Returns:
            typing.Union[typing.Any, None]: returns Base
        """
        if self.base is None:
            self.base = declarative_base()
        return self.base


def _from_results(results) -> typing.Dict:
    """Returns a dictionary for Coding Blocks Podcast

    Args:
        results (FeedParserDict): feedparser results from rss feed

    Returns:
        typing.Dict: parsed dictionary

    TODO: DRY up for other podcasts
    """
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


if __name__ == "__main__":
    pass
