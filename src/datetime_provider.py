import abc


class IDateTimeProvider(abc.ABC):
    @abc.abstractmethod
    def get_now(self):
        pass
