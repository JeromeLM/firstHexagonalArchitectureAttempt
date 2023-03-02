import dataclasses

from src.domain.message_text_exceptions import (
    MessageTextEmptyError,
    MessageTextTooLongError,
)


@dataclasses.dataclass(frozen=True)
class MessageText:
    content: str
    MAX_NB_OF_CHARACTERS_FOR_MESSAGE_TEXT = 280

    def __post_init__(self):
        if self._is_empty():
            raise MessageTextEmptyError()

        if self._is_too_long():
            raise MessageTextTooLongError()

    def _is_empty(self) -> bool:
        text_without_whitespace = "".join(self.content.split())
        return len(text_without_whitespace) == 0

    def _is_too_long(self) -> bool:
        return len(self.content) > self.MAX_NB_OF_CHARACTERS_FOR_MESSAGE_TEXT
