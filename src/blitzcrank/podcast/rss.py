import logging

import feedparser

logger = logging.getLogger(__name__)


def fetch_feed_results(url):
    try:
        return feedparser.parse(url)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    pass
