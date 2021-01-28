"""Podcast server (Discord) gateway
"""

import typing
import logging
from discord import Embed, Webhook, RequestsWebhookAdapter

from .video import Video

logger: logging.Logger = logging.getLogger(__name__)


def publish_video(video: Video, url: str) -> bool:
    """publish_video published a Video object to discord

    Args:
        video (Video): video to publish
        url (str): url to publish to

    Returns:
        bool: True on success
    """
    try:
        embeded = Embed.from_dict(_as_embed(video))
        webhook = Webhook.from_url(
            url,
            adapter=RequestsWebhookAdapter(),
        )
        webhook.send(embed=embeded)
        logger.debug(f"published {video}")
        return True
    except Exception as e:
        logger.error(f"failed to publish {video} -> {e}")
        return False


def _as_embed(video: Video) -> typing.Dict:
    """Returns the podcast as a dictionary for publishing
    to discord

    Args:
        podcast (Podcast): object

    Returns:
        typing.Dict: key/values for discord embed object
    """
    return {
        "id": video.etag,
        # "author": podcast.username, TODO
        "description": video.description,
        "video": video.link,
        "url": video.link,
        "title": video.title,
        "image": {
            "url": video.thumbnails,
        },
    }
