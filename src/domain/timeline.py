import dataclasses
from datetime import datetime
from typing import List

from src.domain.message import Message


@dataclasses.dataclass(frozen=True)
class Timeline:
    messages: List[Message]
    now: datetime

    def get_content(self) -> List[dict]:
        sorted_messages = sorted(
            self.messages, key=lambda x: x.published_at, reverse=True
        )
        return [
            {
                "author": message.author,
                "text": message.text,
                "publishing_time": self._get_publication_time(message.published_at),
            }
            for message in sorted_messages
        ]

    def _get_publication_time(self, published_at: datetime) -> str:
        diff_time_in_minutes = (self.now - published_at).total_seconds() / 60
        if diff_time_in_minutes < 1:
            return "less than 1 minute ago"
        if diff_time_in_minutes >= 1 and diff_time_in_minutes < 2:
            return "1 minute ago"
        return f"{int(diff_time_in_minutes)} minutes ago"
