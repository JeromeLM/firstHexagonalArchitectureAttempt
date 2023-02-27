import abc
from typing import List

from src.message import Message


class IMessageRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, msg: Message):
        pass

    @abc.abstractmethod
    def get_by_id(self, message_id: str) -> Message:
        pass

    @abc.abstractmethod
    def list_messages_by_author(self, author: str) -> List[Message]:
        pass
