from typing import List

from src.post_message_use_case import IMessageRepository


class ViewTimelineUseCase:
    def __init__(self, message_repository: IMessageRepository):
        self.message_repository = message_repository

    def handle(self, author: str) -> List[dict]:
        author_messages = self.message_repository.list_messages_by_author(author)
        author_messages = sorted(
            author_messages, key=lambda x: x.published_at, reverse=True
        )
        # TODO jlm: don't hardcode publishing_time
        return [
            {
                "author": author_messages[0].author,
                "text": author_messages[0].text,
                "publishing_time": "1 minute ago",
            },
            {
                "author": author_messages[1].author,
                "text": author_messages[1].text,
                "publishing_time": "3 minutes ago",
            },
        ]
