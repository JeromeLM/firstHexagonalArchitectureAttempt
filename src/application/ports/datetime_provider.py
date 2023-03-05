import abc
from datetime import datetime


class IDateTimeProvider(abc.ABC):
    @abc.abstractmethod
    def get_now(self) -> datetime:
        pass
