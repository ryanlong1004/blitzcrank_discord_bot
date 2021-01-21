from aiohttp import ClientSession
import logging

logger: logging.Logger = logging.getLogger(__name__)


class LimitExceededWarning(Exception):
    """Exception raised for errors in the input."""

    pass


async def fetch_html(url: str, session: ClientSession, **kwargs):
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html
