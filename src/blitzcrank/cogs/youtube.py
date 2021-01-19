import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, Iterator, List, Tuple

import requests
from discord.ext import commands, tasks
from discord_webhook.webhook import DiscordEmbed, DiscordWebhook

logger: logging.Logger = logging.getLogger(__name__)


class Task:
    def __init__(self, attribs: dict):
        self.webhook_url = attribs["webhook_url"]
        self.api_key = attribs["api_key"]
        self.channel_id = attribs["channel_id"]
        self.etag = attribs["etag"] if "etag" in attribs else None
        self.last_update = attribs["last_update"]
        self.avatar_url = attribs["avatar_url"]
        self.username = attribs["username"]

    def __repr__(self):
        return str(self.__dict__.items())

    def __str__(self):
        return f"<{self.__class__.__name__} {self.username} {self.last_update}>"

    def __iter__(self):
        return iter(self.__dict__.items())

    @staticmethod
    def from_file(_file: str) -> "Task":
        with open(_file, "r") as f:
            return Task(json.load(f))


class Video:
    def __init__(
        self,
        title: str,
        description: str,
        thumbnails: Dict[str, Any],
        publishedAt: str,
        link: str,
        etag: str,
    ):
        self.title = title
        self.description = description
        self.thumbails = thumbnails
        self.publishedAt = publishedAt
        self.link = link
        self.etag = etag

    def __repr__(self):
        return str(self.__dict__.items())

    def __str__(self):
        return f"<{self.__class__.__name__} '{self.title}' {self.link}>"

    @classmethod
    def from_result(cls, result) -> "Video":
        data = result
        meta_data = result["snippet"]

        return Video(
            title=meta_data["title"],
            description=meta_data["description"],
            thumbnails=meta_data["thumbnails"],
            publishedAt=meta_data["publishedAt"],
            link=f"https://youtube.com/watch?v={data['id']['videoId']}",
            etag=data["etag"],
        )


class LimitExceededWarning(Exception):
    """Exception raised for errors in the input."""

    pass


class YouTube(commands.Cog):
    """Cog for getting the latest videos from Youtube channels and sending
    them to their channel via webhook

    Args:
        commands (commands.Cog): Cog base class
    """

    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    @tasks.loop(seconds=60 * 60)
    async def update(self):
        logger.debug("checking for Youtube updates")
        for video, task in _fetch_updates("./src/blitzcrank/cogs/data"):
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


def _fetch_updates(directories: str) -> List[Tuple[Video, Task]]:
    results = []
    for task, file in _load_tasks_from_directory(directories):
        try:
            logger.debug(f"running task {task}")
            video = _get_latest_video_from_task(task)
            time.sleep(5)
            logger.debug(f"stored etag: {task.etag} fetched etag: {video.etag}")
            if task.etag != video.etag:  # new video found
                logger.info(f"New video found {video}")
                task.last_update = datetime.now().isoformat()
                task.etag = video.etag
                logger.debug(f"updating task file with data: {task}")
                _save_task_file(task, file)
                results.append(
                    (video, task),
                )
        except LimitExceededWarning:
            logger.warning("the number of Youtube requests has been exceeded")
            return results
        except Exception as e:
            logger.error(f"Unexpected exception {str(e)}")
            continue
    return results


def _get_latest_video_from_task(task: Task) -> Video:
    return _create_video_from_result(_request(task)[0])


def _create_video_from_result(result) -> Video:
    return Video.from_result(result)


def _save_task_file(task: Task, _file: str) -> None:
    logging.debug(f"Saving data: {task}")
    with open(_file, "w") as __file:
        json.dump(task.__dict__, __file)


def _request(task: Task):
    response = requests.get(_create_fetch_url_from_task(task))
    if response.status_code == 403:
        raise LimitExceededWarning()
    return response.json()["items"]


def _create_fetch_url_from_task(task: Task):
    return f"https://www.googleapis.com/youtube/v3/search?key={task.api_key}&channelId={task.channel_id}&part=snippet,id&order=date&maxResults=20"


def _load_tasks_from_directory(directories: str) -> Iterator[Tuple[Task, str]]:
    abs_directories = [
        os.path.join(directories, _path) for _path in os.listdir(directories)
    ]
    for _file in abs_directories:
        if _file.endswith("_task.json"):
            logging.debug(f"Current file {_file}")
            yield (Task.from_file(_file), _file)
