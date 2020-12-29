from typing import Any, Dict
from discord import Embed, Webhook, RequestsWebhookAdapter


def publish(data: Dict[str, Any], url: str) -> None:
    """Publishes podcast to Discord as embed

    Args:
        data (dict): key/value pair of embeded data
        webhook_url (str): Discord webhook URL
    """

    embeded = Embed.from_dict(data)
    webhook = Webhook.from_url(
        url,
        adapter=RequestsWebhookAdapter(),
    )
    webhook.send(embed=embeded)
