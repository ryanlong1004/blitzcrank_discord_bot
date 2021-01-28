import logging
import json
from typing import List

import requests
from sqlalchemy.sql.sqltypes import JSON

from blitzcrank.database.database import SESSION, ENGINE, BASE
from sqlalchemy.orm.session import Session

from .gateway import fetch_youtube_data
from .task import Task
from .video import Video
from .server import publish_video

logger: logging.Logger = logging.getLogger(__name__)


class LimitExceededWarning(Exception):
    """Exception raised for errors in the input."""

    pass


class Service:
    """YouTube Service"""

    def __init__(self):
        self.session: Session = SESSION()
        BASE.metadata.create_all(ENGINE)

    def fetch_tasks(self) -> List[Task]:
        logger.debug(f"fetching tasks")
        return self.session.query(Task).all()

    def save_task(self, task: Task):
        logger.debug(f"saving task")
        BASE.metadata.create_all(ENGINE)
        self.session.add(task)
        self.session.commit()

    def save_video(self, video: Video):
        logger.debug(f"saving video")
        BASE.metadata.create_all(ENGINE)
        self.session.add(video)
        self.session.commit()

    def run_tasks(self):
        logger.debug(f"running tasks")
        for task in self.fetch_tasks():
            data: list[dict] = fetch_youtube_data(_create_fetch_url_from_task(task))
            if data is None or len(data) < 1:
                continue
            entry_data: dict = fetch_youtube_data(_create_fetch_url_from_task(task))[0]
            video: Video = Video.from_result(entry_data)
            logger.debug(f"fetched {video}")

            logger.debug(f"comparing etags: Task: {task.etag} - Video: {video.etag}")
            if task.etag != video.etag:
                logger.debug(f"found new video {video}")
                task.etag = video.etag
                self.save_task(task)
                self.save_video(video)
                publish_video(video, task.webhook_url)


def _create_fetch_url_from_task(task: Task):
    return f"https://www.googleapis.com/youtube/v3/search?key={task.api_key}&channelId={task.channel_id}&part=snippet,id&order=date&maxResults=20"
