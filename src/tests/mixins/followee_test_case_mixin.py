from typing import List

from src.application.use_cases.follow_user_use_case import (
    FollowUserCommand,
    FollowUserUseCase,
)

from src.domain.followee import Followee
from src.infrastructure.adapters.in_memory_followee_repository import (
    InMemoryFolloweeRepository,
)


class FolloweeTestCaseMixin:
    followee_repository = InMemoryFolloweeRepository()

    def given_user_followees(self, user: str, followees: List[str]):
        existing_followees = [
            Followee(user=user, followee=followee) for followee in followees
        ]
        self.followee_repository.given_existing_followees(existing_followees)

    def when_user_follows_another_user(self, follow_user_command: FollowUserCommand):
        follow_user_use_case = FollowUserUseCase(
            followee_repository=self.followee_repository
        )
        follow_user_use_case.handle(follow_user_command)

    def then_user_followees_should_be(self, expected_user_followees: dict):
        actual_followees = self.followee_repository.list_followees_of_user(
            expected_user_followees["user"]
        )
        assert actual_followees == expected_user_followees["followees"]
