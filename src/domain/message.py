from dataclasses import dataclass, asdict

from src.domain.message_text import MessageText


@dataclass
class Message:
    id: str
    author: str
    text: MessageText
    published_at: str = None

    def __str__(self) -> str:
        return (
            f"Message from {self.author} with id {self.id} and "
            f"containing '{self.text}' was published at {self.published_at}"
        )

    def to_dict(self) -> dict:
        return asdict(self)
