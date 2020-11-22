import os
from typing import Iterator, List, Tuple
import requests
import json
from datetime import datetime

from blitzcrank.cogs.youtube.models.video import Video
from blitzcrank.cogs.youtube.models.task import Task


import logging

logger = logging.getLogger("blitzcrank")


def fetch_updates(directories: List[str]) -> Tuple[Video, Task]:
    for task, file in _load_tasks_from_directory(directories):
        try:
            logger.debug(f"running task {task}")
            video = _get_latest_video_from_task(task)
            if task.etag != video.etag:  # new video found
                task.last_update = datetime.now().isoformat()
                task.etag = video.etag
                logger.debug(f"updating task file with data: {task}")
                task.etag = video.etag
                save_task_file(task, file)
                yield (video, task)
        except LimitExceededWarning:
            logger.warning("the number of Youtube requests has been exceeded")
            return []


def _get_latest_video_from_task(task: Task) -> Video:
    return _create_video_from_result(_request(task)[0])


def _create_video_from_result(result) -> Video:
    return Video.from_result(result)


def save_task_file(task: Task, _file: str) -> None:
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


def _load_tasks_from_directory(directories: List[str]) -> Iterator[Task]:
    abs_directories = [
        os.path.join(directories, _path) for _path in os.listdir(directories)
    ]
    for _file in abs_directories:
        if _file.endswith("_task.json"):
            logging.debug(f"Current file {_file}")
            yield (Task.from_file(_file), _file)


class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class LimitExceededWarning(Error):
    """Exception raised for errors in the input."""

    pass
