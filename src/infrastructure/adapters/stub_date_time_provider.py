from datetime import datetime

from src.application.use_cases.post_message_use_case import IDateTimeProvider


class StubDateTimeProvider(IDateTimeProvider):
    now: datetime

    def get_now(self) -> datetime:
        return self.now
