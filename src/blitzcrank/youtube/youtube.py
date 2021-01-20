import typing

from sqlalchemy.ext.declarative.api import declarative_base

from sqlalchemy import Column, String, DateTime

Base: typing.Any = declarative_base()


class Video(Base):
    """Represents a YouTube Video"""

    __tablename__ = "videos"

    title = Column(String)
    description = Column(String)
    etag = Column(String, primary_key=True)
    thumbnails = Column(String)
    publishedAt = Column("published_at", DateTime, nullable=False)
    link = Column(String)

    @staticmethod
    def from_result(result) -> "Video":
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

    def __repr__(self):
        return str(self.__dict__.items())

    def __str__(self):
        return f"<{self.__class__.__name__} '{self.title}' {self.link}>"
