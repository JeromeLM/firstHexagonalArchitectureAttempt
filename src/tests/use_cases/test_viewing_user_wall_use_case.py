from datetime import datetime
from unittest import TestCase

from src.application.use_cases.view_wall_use_case import ViewWallUseCase
from src.tests.builders.message_builder import MessageBuilder
from src.tests.mixins.followee_test_case_mixin import FolloweeTestCaseMixin
from src.tests.mixins.message_test_case_mixin import MessageTestCaseMixin


class TestViewingUserWallUseCase(FolloweeTestCaseMixin, MessageTestCaseMixin, TestCase):
    """
    Rule: all the messages from the user and his followees must appear in reverse
    chronological order
    """

    wall = []

    def test_user_can_view_his_wall(self):
        self.given_user_followees(user="Bob", followees=["Jane", "David"])
        self.given_following_messages_exist(
            [
                # TODO jlm: how to arrange this formatting ? it's awful !!
                MessageBuilder()
                .written_by("Bob")
                .with_id("message-id-1")
                .with_text("Bob's more recent message")
                .on("2022-06-04T19:16:00")
                .build(),
                MessageBuilder()
                .written_by("Jane")
                .with_id("message-id-2")
                .with_text("Jane's second message")
                .on("2022-06-04T19:04:30")
                .build(),
                MessageBuilder()
                .written_by("Jane")
                .with_id("message-id-3")
                .with_text("Jane's more recent message")
                .on("2022-06-04T19:20:00")
                .build(),
                MessageBuilder()
                .written_by("David")
                .with_id("message-id-4")
                .with_text("David's more recent message")
                .on("2022-06-04T19:14:00")
                .build(),
            ]
        )
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=19, second=30)
        )
        self.when_user_wants_to_see_his_wall(user="Bob")
        self.then_user_should_see_on_his_wall(
            [
                {
                    "author": "Jane",
                    "text": "Jane's more recent message",
                    "publishing_time": "less than 1 minute ago",
                },
                {
                    "author": "Bob",
                    "text": "Bob's more recent message",
                    "publishing_time": "3 minutes ago",
                },
                {
                    "author": "David",
                    "text": "David's more recent message",
                    "publishing_time": "5 minutes ago",
                },
                {
                    "author": "Jane",
                    "text": "Jane's second message",
                    "publishing_time": "15 minutes ago",
                },
            ]
        )

    def when_user_wants_to_see_his_wall(self, user: str):
        view_wall_use_case = ViewWallUseCase(
            message_repository=self.message_repository,
            followee_repository=self.followee_repository,
            date_time_provider=self.date_time_provider,
        )
        self.wall = view_wall_use_case.handle(user="Bob")

    def then_user_should_see_on_his_wall(self, expected_wall):
        assert self.wall == expected_wall
