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
    published_at = Column("published_at", DateTime, nullable=False)
    link = Column(String)

    def __init__(
        self,
        title: str,
        description: str,
        etag: str,
        thumbnails: str,
        published_at: str,
        link: str,
    ):
        self.title = title
        self.description = description
        self.etag = etag
        self.thumbnails = thumbnails
        self.published_at = published_at
        self.link = link

    @staticmethod
    def from_result(result) -> "Video":
        data = result
        meta_data = result["snippet"]

        return Video(
            title=meta_data["title"],
            description=meta_data["description"],
            etag=data["etag"],
            thumbnails=meta_data["thumbnails"],
            published_at=meta_data["publishedAt"],
            link=f"https://youtube.com/watch?v={data['id']['videoId']}",
        )

    def __repr__(self):
        return str(self.__dict__.items())

    def __str__(self):
        return f"<{self.__class__.__name__} '{self.title}' {self.link}>"
