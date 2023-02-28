import json
from typing import List

from src.message import Message
from src.message_repository import IMessageRepository


class FileSystemMessageRepository(IMessageRepository):
    filename = "temporary.json"

    def save(self, msg: Message):
        messages = self._list_messages()
        messages.append(msg.to_dict())
        with open(self.filename, "w") as f:
            json.dump(messages, f)

    def get_by_id(self, message_id: str) -> Message:
        with open(self.filename, "r") as f:
            messages = self._list_messages()
            message = next(
                message for message in messages if message["id"] == message_id
            )
            return Message(
                id=message["id"],
                text=message["text"],
                author=message["author"],
                published_at=message["published_at"],
            )

    def list_messages_by_author(self, author: str) -> List[Message]:
        messages = self._list_messages()
        return [
            Message(
                id=message["id"],
                text=message["text"],
                author=message["author"],
                published_at=message["published_at"],
            )
            for message in messages
            if message["author"] == author
        ]

    def _list_messages(self) -> List[dict]:
        with open(self.filename, "r") as f:
            messages = json.load(f)
            return [
                {
                    "id": message["id"],
                    "text": message["text"],
                    "author": message["author"],
                    "published_at": message["published_at"],
                }
                for message in messages
            ]
