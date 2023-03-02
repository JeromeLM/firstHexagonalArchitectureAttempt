from dataclasses import dataclass

from src.application.ports.datetime_provider import IDateTimeProvider
from src.domain.message import Message
from src.application.ports.message_repository import IMessageRepository
from src.domain.message_text import MessageText


@dataclass
class PostMessageCommand:
    id: str
    text: str
    author: str


class PostMessageUseCase:
    def __init__(
        self,
        message_repository: IMessageRepository,
        date_time_provider: IDateTimeProvider,
    ):
        self.message_repository = message_repository
        self.date_time_provider = date_time_provider

    def handle(self, message_command: PostMessageCommand):
        message_text = MessageText(content=message_command.text)
        message = Message(
            id=message_command.id,
            text=message_text,
            author=message_command.author,
            published_at=self.date_time_provider.get_now(),
        )
        self.message_repository.save(message)
