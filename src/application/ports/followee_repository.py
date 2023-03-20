import abc
from typing import List

from src.domain.followee import Followee


class IFolloweeRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, followee: Followee):
        pass

    @abc.abstractmethod
    def list_followees_of_user(self, user: str) -> List[str]:
        pass
