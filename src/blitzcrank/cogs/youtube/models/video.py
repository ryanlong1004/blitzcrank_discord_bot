from typing import Any, Dict


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