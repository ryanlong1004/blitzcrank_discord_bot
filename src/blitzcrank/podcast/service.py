import datetime
import logging
import re
import typing

from blitzcrank.database.database import BASE, ENGINE, SESSION
from sqlalchemy.orm.session import Session

from .podcast import Podcast
from .rss import fetch_feed_results
from .server import publish_podcast

logger: logging.Logger = logging.getLogger(__name__)


class Service:
    """Podcast Service"""

    def __init__(self):
        self.session: Session = SESSION()
        BASE.metadata.create_all(ENGINE)

    def save(self, podcast: Podcast) -> Podcast:
        """Saves a podcast to persistence

        Args:
            podcast (Podcast): object
        """
        logger.debug(f"saving {self.__class__} {podcast}")
        BASE.metadata.create_all(ENGINE)
        self.session.add(podcast)
        self.session.commit()
        return self.fetch_last_local()

    def fetch_last_local(self) -> Podcast:
        """Returns the last podcast collected from remote by created
        date in descending order.

        Returns:
            Podcast: object
        """
        logger.debug(f"fetching last local {self.__class__}")
        return self.session.query(Podcast).order_by(Podcast.created_at.desc())[0]

    @staticmethod
    def publish(podcast: Podcast, url: str) -> bool:
        """Publishes podcast to url

        Args:
            podcast (Podcast): object
            url (str): webhook url to publish to
        """
        logger.debug(f"publishing {podcast}")
        return publish_podcast(podcast, url)

    def fetch_last_remote(self) -> Podcast:
        """Returns the last remote podcast from the RSS feed based
        on the first value returned.

        Returns:
            Podcast: object
        """
        logging.debug(f"fetching last remote {self.__class__}")
        return Podcast.from_result(
            fetch_feed_results("https://www.codingblocks.net/feed/podcast")
        )

    def run_tasks(self):
        logger.debug("checking for RSS updates")
        podcast: Podcast = self.fetch_last_remote()
        last: Podcast = self.fetch_last_local()
        if podcast.id != last.id:
            try:
                self.publish(
                    podcast,
                    "https://discord.com/api/webhooks/793195455194333186/Kvie1rOoBa28XyKb15epsnZmQ0EIQ16GnSonJ8Gfi1K4Wpn907mIcRpjRlhM6fCAKPrh",
                )
                self.save(podcast)  # TODO Will need error handling
            except Exception as e:
                logger.error(f"publish podcast failed: {e} - {podcast}")


if __name__ == "__main__":
    pass
