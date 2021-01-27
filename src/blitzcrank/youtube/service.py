import logging
import typing
from datetime import datetime
from typing import List

from blitzcrank.database.database import Database
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from .gateway import fetch_html
from .task import Task
from .video import Video
from .server import publish_video

logger: logging.Logger = logging.getLogger(__name__)


class LimitExceededWarning(Exception):
    """Exception raised for errors in the input."""

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

    def save_task(self, task: Task):
        super().get_base().metadata.create_all(super().get_engine())
        super().get_session().add(task)
        super().get_session().commit()

    def save_video(self, video: Video):
        super().get_base().metadata.create_all(super().get_engine())
        super().get_session().add(video)
        super().get_session().commit()

    def run_tasks(self):
        for task in self.fetch_tasks():
            html = fetch_html(_create_fetch_url_from_task(task))
            video = Video.from_result(html)
            if task.etag != video.etag:
                print("***********************")
                print("PROCESSING ETAG")
                logger.debug("PROCESSING ETAG")
                self.save_video(video)
                task.etag = video.etag
                publish_video(video, task.webhook_url)

    # def fetch_updates():
    #     # tasks = Task.
    #     results = []
    #     for task, file in _load_tasks_from_directory():
    #         try:
    #             logger.debug(f"running task {task}")
    #             video = _get_latest_video_from_task(task)
    #             time.sleep(5)
    #             logger.debug(f"stored etag: {task.etag} fetched etag: {video.etag}")
    #             if task.etag != video.etag:  # new video found
    #                 logger.info(f"New video found {video}")
    #                 task.last_update = datetime.now().isoformat()
    #                 task.etag = video.etag
    #                 logger.debug(f"updating task file with data: {task}")
    #                 # _save_task_file(task, file)
    #                 results.append(
    #                     (video, task),
    #                 )
    #         except LimitExceededWarning:
    #             logger.warning("the number of Youtube requests has been exceeded")
    #             return results
    #         except Exception as e:
    #             logger.error(f"Unexpected exception {str(e)}")
    #             continue
    # return results


# def _request(task: Task):
#     response = requests.get(_create_fetch_url_from_task(task))
#     if response.status_code == 403:
#         raise LimitExceededWarning()
#     return response.json()["items"]


def _create_fetch_url_from_task(task: Task):
    return f"https://www.googleapis.com/youtube/v3/search?key={task.api_key}&channelId={task.channel_id}&part=snippet,id&order=date&maxResults=20"
