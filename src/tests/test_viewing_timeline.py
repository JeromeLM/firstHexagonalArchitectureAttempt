from datetime import datetime
from unittest import TestCase

from src.message import Message
from src.tests.mixins.message_test_case_mixin import MessageTestCaseMixin


class TestViewingTimeline(MessageTestCaseMixin, TestCase):

    """
    Rule: messages are displayed in reverse chronological order
    """

    def test_user_Bob_can_view_the_2_messages_he_published_in_his_timeline(self):
        self.given_following_messages_exist(
            [
                Message(
                    author="Bob",
                    id="message-id-1",
                    text="Bob's first message",
                    published_at="2022-06-04T19:00:00",
                ),
                Message(
                    author="Jane",
                    id="message-id-2",
                    text="Jane's first message",
                    published_at="2022-06-04T19:01:00",
                ),
                Message(
                    author="Bob",
                    id="message-id-3",
                    text="Bob's second message",
                    published_at="2022-06-04T19:02:00",
                ),
                Message(
                    author="Bob",
                    id="message-id-4",
                    text="Bob's last message",
                    published_at="2022-06-04T19:02:20",
                ),
            ]
        )
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=3, second=0)
        )
        self.when_user_wants_to_view_his_timeline(author="Bob")
        self.then_displayed_timeline_should_be(
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
