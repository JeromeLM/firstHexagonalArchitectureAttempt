import json
import os.path
from datetime import datetime
from typing import List

from src.domain.message import Message
from src.application.ports.message_repository import IMessageRepository
from src.domain.message_text import MessageText


class FileSystemMessageRepository(IMessageRepository):
    filepath = os.path.abspath("./messages.json")

    def __init__(self, filepath=None):
        if filepath:
            self.filepath = filepath

    def save(self, message: Message):
        messages = self._list_messages()
        try:
            existing_message_index = next(
                index for index, msg in enumerate(messages) if msg["id"] == message.id
            )
            messages[existing_message_index]["text"] = message.text
            messages[existing_message_index][
                "published_at"
            ] = message.published_at.isoformat()
        except StopIteration:
            messages.append({**message.to_dict()})

        with open(self.filepath, "w") as f:
            json.dump(messages, f)

    def get_by_id(self, message_id: str) -> Message:
        # TODO jlm: manage case id is not found (StopIteration)
        messages = self._list_messages()
        message = next(message for message in messages if message["id"] == message_id)
        return Message.create_from_data(message)

    def list_messages_by_author(self, author: str) -> List[Message]:
        messages = self._list_messages()
        return [
            Message.create_from_data(message)
            for message in messages
            if message["author"] == author
        ]

    def _list_messages(self) -> List[dict]:
        with open(self.filepath, "r") as f:
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
