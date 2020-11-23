import json


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

    def from_file(_file: str) -> "Task":
        with open(_file, "r") as f:
            return Task(json.load(f))