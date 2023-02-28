from dataclasses import dataclass

from src.datetime_provider import IDateTimeProvider
from src.message import Message
from src.message_repository import IMessageRepository


@dataclass
class PostMessageCommand:
    id: str
    text: str
    author: str


class MessageTextTooLongError(Exception):
    pass


class MessageTextEmptyError(Exception):
    pass


class PostMessageUseCase:
    MAX_NB_OF_CHARACTERS_FOR_MESSAGE_TEXT = 280

    def __init__(
        self,
        message_repository: IMessageRepository,
        date_time_provider: IDateTimeProvider,
    ):
        self.message_repository = message_repository
        self.date_time_provider = date_time_provider

    def handle(self, message_command: PostMessageCommand):
        if self._is_message_text_empty(message_command.text):
            raise MessageTextEmptyError()

        if self._is_message_text_too_long(message_command.text):
            raise MessageTextTooLongError()

        message = Message(
            id=message_command.id,
            text=message_command.text,
            author=message_command.author,
            published_at=self.date_time_provider.get_now(),
        )
        self.message_repository.save(message)

    def _is_message_text_empty(self, message_text: str) -> bool:
        text_without_whitespace = "".join(message_text.split())
        return len(text_without_whitespace) == 0

    def _is_message_text_too_long(self, message_text: str) -> bool:
        return len(message_text) > self.MAX_NB_OF_CHARACTERS_FOR_MESSAGE_TEXT
