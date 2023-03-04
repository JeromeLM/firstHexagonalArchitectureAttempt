from datetime import datetime

from src.application.ports.datetime_provider import IDateTimeProvider


class RealDateTimeProvider(IDateTimeProvider):
    def get_now(self):
        return datetime.now().isoformat()
