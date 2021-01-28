"""Podcast RSS gateway
"""
import logging
import typing

import feedparser
from feedparser.util import FeedParserDict

logger: logging.Logger = logging.getLogger(__name__)


def fetch_feed_results(url: str) -> typing.Optional[FeedParserDict]:
    """Returns the raw rss results from the url

    Args:
        url (str): URL to fetch

    Returns:
        FeedParserDict: rss results
    """
    logger.debug("fetching feed results")
    try:
        return feedparser.parse(url)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    pass
