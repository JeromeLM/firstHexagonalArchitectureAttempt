import json

from src.post_message_use_case import IMessageRepository, Message


class FileSystemMessageRepository(IMessageRepository):
    filename = "temporary.txt"

    def save(self, msg: Message):
        with open(self.filename, "w") as f:
            f.write(json.dumps(msg.to_dict()))

    def get(self) -> Message:
        with open(self.filename, "r") as f:
            file_content = json.loads(f.read())
            return Message(
                id=file_content["id"],
                text=file_content["text"],
                author=file_content["author"],
                published_at=file_content["published_at"],
            )
