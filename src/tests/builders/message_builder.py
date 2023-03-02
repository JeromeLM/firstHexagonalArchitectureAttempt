# TODO jlm: not really sure about this...
# TODO jlm: Is it right to create multiple instances in a row ?!
from dataclasses import dataclass, asdict
from datetime import datetime

from src.message import Message
from src.message_text import MessageText


@dataclass
class MessageBuilder:
    id: str = "message id"
    author: str = "John Doe"
    text: str = "this is a text"
    published_at: str = datetime(year=2022, month=6, day=4, hour=19, minute=3, second=0)

    def with_id(self, id: str):
        return MessageBuilder(**{**asdict(self), "id": id})

    def written_by(self, author: str):
        return MessageBuilder(**{**asdict(self), "author": author})

    def with_text(self, text: str):
        return MessageBuilder(**{**asdict(self), "text": text})

    def on(self, published_at: str):
        return MessageBuilder(**{**asdict(self), "published_at": published_at})

    def build(self):
        return Message(
            id=self.id,
            author=self.author,
            text=MessageText(self.text),
            published_at=self.published_at,
        )
