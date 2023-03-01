import copy
from typing import List

from src.message import Message
from src.message_repository import IMessageRepository


class InMemoryMessageRepository(IMessageRepository):
    messages = {}

    def save(self, msg: Message):
        self.messages[msg.id] = msg

    def get_by_id(self, message_id: str) -> Message:
        return copy.deepcopy(self.messages.get(message_id))

    def list_messages_by_author(self, author: str) -> List[Message]:
        return [
            message
            for message_id, message in self.messages.items()
            if message.author == author
        ]

    def given_existing_messages(self, messages: List[Message]):
        self.messages = {message.id: message for message in messages}
