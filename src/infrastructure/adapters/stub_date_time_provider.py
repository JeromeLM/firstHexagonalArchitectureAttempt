from datetime import datetime

from src.application.use_cases.post_message_use_case import IDateTimeProvider


class StubDateTimeProvider(IDateTimeProvider):
    now: datetime

    def get_now(self) -> str:
        return self.now.isoformat()
