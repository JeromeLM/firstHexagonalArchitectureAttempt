from unittest import TestCase

from src.application.use_cases.follow_user_use_case import FollowUserCommand
from src.tests.mixins.followee_test_case_mixin import FolloweeTestCaseMixin


class TestFollowingUser(FolloweeTestCaseMixin, TestCase):
    def test_user_can_follow_another_user(self):
        self.given_user_followees(user="Bob", followees=["Jane"])
        self.when_user_follows_another_user(
            FollowUserCommand(user="Bob", user_to_follow="David")
        )
        self.then_user_followees_should_be(
            {"user": "Bob", "followees": ["Jane", "David"]}
        )
