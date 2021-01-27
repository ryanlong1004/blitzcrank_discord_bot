import requests

import logging

logger: logging.Logger = logging.getLogger(__name__)


class LimitExceededWarning(Exception):
    """Exception raised for errors in the input."""

    pass


async def fetch_html(url: str):
    return requests.get(url).text
