import datetime
import logging
import re
import typing

import feedparser
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from .podcast import Podcast
from .rss import fetch_feed_results
from .server import publish_podcast

logger = logging.getLogger(__name__)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class Service:
    def __init__(self, session=None, engine=None, base=None):
        self.session: typing.Optional[Session] = session
        self.engine: typing.Optional[Engine] = engine
        self.base: typing.Optional[typing.Any] = base

    def save(self, podcast: Podcast):
        self._get_base().metadata.create_all(self._get_engine())
        self._get_session().add(podcast)
        self._get_session().commit()

    def last(self):
        return self._get_session().query(Podcast).order_by(Podcast.created_at.desc())[0]

    def publish(self, podcast: Podcast, url):
        publish_podcast(podcast, url)

    def fetch_recent_podcast(self):
        return Podcast(
            **from_results(
                fetch_feed_results("https://www.codingblocks.net/feed/podcast")
            )
        )

    def _get_session(self):
        if self.session is None:
            Session = sessionmaker()
            Session.configure(bind=self._get_engine())
            self.session = Session()
        return self.session

    def _get_engine(self):
        if self.engine is None:
            self.engine = create_engine(f"sqlite:///test.db")
        return self.engine

    def _get_base(self):
        if self.base is None:
            self.base = declarative_base()
        return self.base


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


if __name__ == "__main__":
    pass
