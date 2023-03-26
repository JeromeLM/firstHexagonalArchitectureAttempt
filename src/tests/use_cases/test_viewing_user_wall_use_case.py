from datetime import datetime
from unittest import TestCase

from src.tests.builders.message_builder import MessageBuilder
from src.tests.fixtures.followee_fixture import FolloweeFixture
from src.tests.fixtures.message_fixture import MessageFixture
from src.tests.fixtures.wall_fixture import WallFixture


class TestViewingUserWallUseCase(TestCase):
    def setUp(self) -> None:
        self.message_fixture = MessageFixture()
        self.followee_fixture = FolloweeFixture()
        self.wall_fixture = WallFixture(
            message_repository=self.message_fixture.message_repository,
            followee_repository=self.followee_fixture.followee_repository,
        )

    """
    Rule: all the messages from the user and his followees must appear in reverse
    chronological order
    """

    def test_user_can_view_his_wall(self):
        self.followee_fixture.given_user_followees(
            user="Bob", followees=["Jane", "David"]
        )
        self.message_fixture.given_following_messages_exist(
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
        self.wall_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=19, second=30)
        )
        self.wall_fixture.when_user_wants_to_see_his_wall(user="Bob")
        self.wall_fixture.then_user_should_see_on_his_wall(
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
