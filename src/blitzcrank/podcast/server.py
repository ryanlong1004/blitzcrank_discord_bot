"""Podcast server (Discord) gateway
"""

import typing
from discord import Embed, Webhook, RequestsWebhookAdapter

from .podcast import Podcast


def publish_podcast(podcast: Podcast, url: str) -> None:
    """Publishes podcast to Discord as embed

    Args:
        data (dict): key/value pair of embeded data
        webhook_url (str): Discord webhook URL
    """
    embeded = Embed.from_dict(_as_embed(podcast))
    webhook = Webhook.from_url(
        url,
        adapter=RequestsWebhookAdapter(),
    )
    webhook.send(embed=embeded)


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
