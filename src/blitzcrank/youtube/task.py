import logging
import typing

from requests import api
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative.api import declarative_base

Base: typing.Any = declarative_base()

logger: logging.Logger = logging.getLogger(__name__)


class Task(Base):
    """Represents a task to fetch a YouTube Video"""

    __tablename__ = "tasks"

    etag = Column(String, primary_key=True)
    webhook_url = Column(String)
    api_key = Column(String)
    channel_id = Column(String)
    last_update = Column("last_update", DateTime, nullable=False)
    username = Column(String)
    avatar_url = Column(String)

    def __init__(
        self,
        etag: str,
        webhook_url: str,
        api_key: str,
        channel_id: str,
        last_update: DateTime,
        username: str,
        avatar_url: str,
    ):
        self.etag = etag
        self.webhook_url = webhook_url
        self.api_key = api_key
        self.channel_id = channel_id
        self.last_update = last_update
        self.username = username
        self.avatar_url = avatar_url

    def __repr__(self):
        return str(self.__dict__.items())

    def __str__(self):
        return f"<{self.__class__.__name__} '{self.etag}' {self.channel_id}>"
