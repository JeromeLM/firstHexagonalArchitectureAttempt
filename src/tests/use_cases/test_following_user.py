from unittest import TestCase

from src.application.use_cases.follow_user_use_case import FollowUserCommand
from src.tests.fixtures.followee_fixture import FolloweeFixture


class TestFollowingUser(TestCase):
    def setUp(self) -> None:
        self.followee_fixture = FolloweeFixture()

    def test_user_can_follow_another_user(self):
        self.followee_fixture.given_user_followees(user="Bob", followees=["Jane"])
        self.followee_fixture.when_user_follows_another_user(
            FollowUserCommand(user="Bob", user_to_follow="David")
        )
        self.followee_fixture.then_user_followees_should_be(
            {"user": "Bob", "followees": ["Jane", "David"]}
        )
