import json
from typing import List

from src.message import Message
from src.message_repository import IMessageRepository


class FileSystemMessageRepository(IMessageRepository):
    filename = "temporary.json"

    def save(self, message: Message):
        messages = self._list_messages()
        try:
            existing_message_index = next(
                index for index, msg in enumerate(messages) if msg["id"] == message.id
            )
            messages[existing_message_index]["text"] = message.text
        except StopIteration:
            messages.append(message.to_dict())

        with open(self.filename, "w") as f:
            json.dump(messages, f)

    def get_by_id(self, message_id: str) -> Message:
        # TODO jlm: manage case id is not found (StopIteration)
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
