import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord_webhook.webhook import DiscordEmbed, DiscordWebhook
from blitzcrank.cogs.youtube.models.video import Video
from blitzcrank.cogs.youtube.models.task import Task
from blitzcrank.cogs.youtube import fetch_updates

import logging

logger = logging.getLogger("blitzcrank")


class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    @tasks.loop(seconds=60 * 15)
    async def update(self):
        logger.debug("checking for Youtube updates")
        for video, task in fetch_updates("./src/blitzcrank/cogs/youtube/data"):
            print(video)
            self.publish(video, task)

    @update.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

    def publish(self, video: Video, task: Task):
        webhook = DiscordWebhook(url=task.webhook_url)
        webhook.avatar_url = task.avatar_url
        webhook.username = task.username

        embed = DiscordEmbed(
            title=video.title, description=video.description, color=2552190
        )
        embed.set_timestamp()
        embed.set_image(url=video.thumbails["high"]["url"])
        embed.set_url(url=video.link)

        webhook.add_embed(embed)
        webhook.execute()