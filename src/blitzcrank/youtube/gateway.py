import logging
import typing

import requests

logger: logging.Logger = logging.getLogger(__name__)


def fetch_youtube_data(url: str) -> typing.List[dict]:
    """fetch_rss_data takes a url and fetches the response as a list of dicts

    Args:
        url (str): URL to fetch youtube data

    Returns:
        list: list of dictionary results
    """
    logger.debug(f"fetching from url: {url}")
    try:
        return requests.get(url).json()["items"]
    except Exception as e:
        logger.debug(f"failed to fetch youtube data -> {e}")
        return []
