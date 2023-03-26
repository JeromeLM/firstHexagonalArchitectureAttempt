from datetime import datetime
from unittest import TestCase

from src.tests.builders.message_builder import MessageBuilder
from src.tests.fixtures.message_fixture import MessageFixture


class TestViewingTimeline(TestCase):
    def setUp(self) -> None:
        self.message_fixture = MessageFixture()

    """
    Rule: messages are displayed in reverse chronological order
    """

    def test_user_Bob_can_view_the_2_messages_he_published_in_his_timeline(self):
        self.message_fixture.given_following_messages_exist(
            [
                # TODO jlm: how to arrange this formatting ? it's awful !!
                MessageBuilder()
                .written_by("Bob")
                .with_id("message-id-1")
                .with_text("Bob's first message")
                .on("2022-06-04T19:00:00")
                .build(),
                MessageBuilder()
                .written_by("Jane")
                .with_id("message-id-2")
                .with_text("Jane's first message")
                .on("2022-06-04T19:01:00")
                .build(),
                MessageBuilder()
                .written_by("Bob")
                .with_id("message-id-3")
                .with_text("Bob's second message")
                .on("2022-06-04T19:02:00")
                .build(),
                MessageBuilder()
                .written_by("Bob")
                .with_id("message-id-4")
                .with_text("Bob's last message")
                .on("2022-06-04T19:02:20")
                .build(),
            ]
        )
        self.message_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=3, second=0)
        )
        self.message_fixture.when_user_wants_to_view_his_timeline(author="Bob")
        self.message_fixture.then_displayed_timeline_should_be(
            [
                {
                    "author": "Bob",
                    "text": "Bob's last message",
                    "publishing_time": "less than 1 minute ago",
                },
                {
                    "author": "Bob",
                    "text": "Bob's second message",
                    "publishing_time": "1 minute ago",
                },
                {
                    "author": "Bob",
                    "text": "Bob's first message",
                    "publishing_time": "3 minutes ago",
                },
            ]
        )
