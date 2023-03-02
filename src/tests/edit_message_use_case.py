from dataclasses import dataclass

from src.datetime_provider import IDateTimeProvider
from src.message import Message
from src.message_repository import IMessageRepository
from src.message_text import MessageText


@dataclass
class EditMessageCommand:
    id: str
    text: str
    author: str


class EditMessageUseCase:
    def __init__(
        self,
        message_repository: IMessageRepository,
        date_time_provider: IDateTimeProvider,
    ):
        self.message_repository = message_repository
        self.date_time_provider = date_time_provider

    def handle(self, message_command: EditMessageCommand):
        # TODO jlm: check author
        message_text = MessageText(content=message_command.text)
        message = self.message_repository.get_by_id(message_command.id)
        self.message_repository.save(
            Message(
                id=message.id,
                author=message.author,
                text=message_text,
                published_at=self.date_time_provider.get_now(),
            )
        )
