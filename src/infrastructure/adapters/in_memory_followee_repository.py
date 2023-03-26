import copy
from typing import List

from src.application.ports.followee_repository import IFolloweeRepository
from src.domain.followee import Followee


class InMemoryFolloweeRepository(IFolloweeRepository):
    def __init__(self):
        self.followees_by_user = {}

    def save(self, followee: Followee):
        self._add_followee(followee)

    def list_followees_of_user(self, user: str) -> List[str]:
        return copy.deepcopy(self.followees_by_user.get(user, []))

    def given_existing_followees(self, existing_followees: List[Followee]):
        for followee in existing_followees:
            self._add_followee(followee)

    def _add_followee(self, followee: Followee):
        existing_followees = self.followees_by_user.get(followee.user, [])
        existing_followees.append(followee.followee)
        self.followees_by_user[followee.user] = existing_followees
