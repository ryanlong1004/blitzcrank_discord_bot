import typing

from sqlalchemy.ext.declarative.api import declarative_base

from sqlalchemy import Column, String, DateTime

Base: typing.Any = declarative_base()


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

    def __repr__(self):
        return str(self.__dict__.items())

    def __str__(self):
        return f"<{self.__class__.__name__} '{self.etag}' {self.channel_id}>"
