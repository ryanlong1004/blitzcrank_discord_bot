import json
import logging
import time
from datetime import datetime
from typing import List, Tuple
import typing

from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine

import requests

from blitzcrank.database.database import Database

from .task import Task
from .youtube import Video

logger: logging.Logger = logging.getLogger(__name__)


class LimitExceededWarning(Exception):
    """Exception raised for errors in the input."""

    pass


def fetch_tasks():
    pass


class Service(Database):
    """YouTube Service"""

    def __init__(
        self,
        session: typing.Union[Session, None] = None,
        engine: typing.Union[Engine, None] = None,
        base: typing.Union[typing.Any, None] = None,
    ):
        """Initizalize service.  Vars are for testing.

        Args:
            session (Session, None): Session object. Defaults to None.
            engine (Engine, None): Engine object. Defaults to None.
            base (Base, None): Base object. Defaults to None.
        """
        super().__init__(session, engine, base)

    def fetch_tasks(self) -> List[Task]:
        return super().get_session().query(Task).all()

    def run_tasks(self):
        for task in self.fetch_tasks():
            pass


def fetch_updates():
    # tasks = Task.
    results = []
    for task, file in _load_tasks_from_directory():
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
                # _save_task_file(task, file)
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


def _load_tasks_from_directory():
    return []


def _get_latest_video_from_task(task: Task) -> Video:
    return _create_video_from_result(_request(task)[0])


def _create_video_from_result(result) -> Video:
    return Video.from_result(result)


def _request(task: Task):
    response = requests.get(_create_fetch_url_from_task(task))
    if response.status_code == 403:
        raise LimitExceededWarning()
    return response.json()["items"]


def _create_fetch_url_from_task(task: Task):
    return f"https://www.googleapis.com/youtube/v3/search?key={task.api_key}&channelId={task.channel_id}&part=snippet,id&order=date&maxResults=20"
