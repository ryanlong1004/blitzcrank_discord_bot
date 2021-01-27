"""Podcast server (Discord) gateway
"""

import typing
from discord import Embed, Webhook, RequestsWebhookAdapter

from .video import Video


def publish_video(video: Video, url: str) -> None:
    """Publishes podcast to Discord as embed

    Args:
        data (dict): key/value pair of embeded data
        webhook_url (str): Discord webhook URL
    """
    embeded = Embed.from_dict(_as_embed(video))
    webhook = Webhook.from_url(
        url,
        adapter=RequestsWebhookAdapter(),
    )
    webhook.send(embed=embeded)


def _as_embed(video: Video) -> typing.Dict:
    """Returns the podcast as a dictionary for publishing
    to discord

    Args:
        podcast (Podcast): object

    Returns:
        typing.Dict: key/values for discord embed object
    """
    return {
        "id": video.id,
        "description": video.description,
        "url": video.url,
        "title": video.title,
        "image": {
            "url": video.image,
        },
    }
