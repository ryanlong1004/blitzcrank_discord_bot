"""Podcast server (Discord) gateway
"""

import logging
import typing

from discord import Embed, RequestsWebhookAdapter, Webhook

from .podcast import Podcast

logger: logging.Logger = logging.getLogger(__name__)


def publish_podcast(podcast: Podcast, url: str) -> bool:
    """Publishes podcast to Discord as embed

    Args:
        data (dict): key/value pair of embeded data
        webhook_url (str): Discord webhook URL
    """
    logger.debug(f"publishing podcast {podcast}")
    try:
        embeded = Embed.from_dict(_as_embed(podcast))
        webhook = Webhook.from_url(
            url,
            adapter=RequestsWebhookAdapter(),
        )
        webhook.send(embed=embeded)
        logger.debug(f"published podcast {podcast}")
        return True
    except Exception as e:
        return False


def _as_embed(podcast: Podcast) -> typing.Dict:
    """Returns the podcast as a dictionary for publishing
    to discord

    Args:
        podcast (Podcast): object

    Returns:
        typing.Dict: key/values for discord embed object
    """
    return {
        "id": podcast.id,
        "description": podcast.description,
        "url": podcast.url,
        "title": podcast.title,
        "image": {
            "url": podcast.image,
        },
    }
