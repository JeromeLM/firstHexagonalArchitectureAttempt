from src.post_message_use_case import IMessageRepository, Message


class InMemoryMessageRepository(IMessageRepository):
    def save(self, msg: Message):
        self.message = msg

    def get(self) -> Message:
        return self.message
