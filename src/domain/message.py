from dataclasses import dataclass
from datetime import datetime

from src.domain.message_text import MessageText


@dataclass
class Message:
    _id: str
    _author: str
    _text: MessageText
    _published_at: datetime = None

    def __str__(self) -> str:
        return (
            f"Message from {self._author} with id {self._id} and "
            f"containing '{self._text.content}' was published at {self._published_at}"
        )

    @property
    def id(self) -> str:
        return self._id

    @property
    def author(self) -> str:
        return self._author

    @property
    def text(self) -> str:
        return self._text.content

    # TODO jlm: not sure whether it's better to return a datetime or a string
    @property
    def published_at(self) -> datetime:
        return self._published_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "published_at": self.published_at.isoformat(),
        }

    # Factory method -- to use instead of direct instantiation !
    @classmethod
    def create_from_data(cls, data: dict):
        published_at = (
            data["published_at"]
            if isinstance(data["published_at"], datetime)
            else datetime.fromisoformat(data["published_at"])
        )
        return cls(
            _id=data["id"],
            _author=data["author"],
            _text=MessageText(data["text"]),
            _published_at=published_at,
        )
