from datetime import datetime
from typing import List

from src.application.ports.datetime_provider import IDateTimeProvider
from src.application.ports.message_repository import IMessageRepository


class ViewTimelineUseCase:
    def __init__(
        self,
        message_repository: IMessageRepository,
        date_time_provider: IDateTimeProvider,
    ):
        self.message_repository = message_repository
        self.date_time_provider = date_time_provider

    def handle(self, author: str) -> List[dict]:
        author_messages = self.message_repository.list_messages_by_author(author)
        author_messages = sorted(
            author_messages, key=lambda x: x.published_at, reverse=True
        )
        return [
            {
                "author": message.author,
                "text": message.text,
                "publishing_time": self._get_publication_time(message.published_at),
            }
            for message in author_messages
        ]

    def _get_publication_time(self, published_at: datetime) -> str:
        now = self.date_time_provider.get_now()
        diff_time_in_minutes = (now - published_at).total_seconds() / 60
        if diff_time_in_minutes < 1:
            return "less than 1 minute ago"
        if diff_time_in_minutes >= 1 and diff_time_in_minutes < 2:
            return "1 minute ago"
        return f"{int(diff_time_in_minutes)} minutes ago"
