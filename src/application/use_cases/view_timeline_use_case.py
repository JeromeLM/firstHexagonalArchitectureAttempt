from typing import List

from src.application.ports.datetime_provider import IDateTimeProvider
from src.application.ports.message_repository import IMessageRepository
from src.domain.timeline import Timeline


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
        timeline = Timeline(
            messages=author_messages, now=self.date_time_provider.get_now()
        )
        return timeline.get_content()
