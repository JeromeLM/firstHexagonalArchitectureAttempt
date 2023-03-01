from datetime import datetime
from unittest import TestCase

from src.message import Message
from src.post_message_use_case import MessageTextTooLongError, MessageTextEmptyError
from src.tests.edit_message_use_case import EditMessageCommand
from src.tests.mixins.message_test_case_mixin import MessageTestCaseMixin


class TestEditingMessage(MessageTestCaseMixin, TestCase):
    edited_message = None

    """
    Rule: a message must have a max length of 280 characters
    """

    def test_user_can_edit_a_message_on_his_timeline(self):
        self.given_following_messages_exist(
            [
                Message(
                    author="Bob",
                    id="message-id-4",
                    text="Bob's last message",
                    published_at="2022-06-04T19:02:20",
                ),
            ]
        )
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=10, second=0)
        )
        self.when_user_edits_message(
            EditMessageCommand(
                author="Bob",
                id="message-id-4",
                text="Bob's edited message",
            )
        )
        self.then_edited_message_should_be(
            Message(
                author="Bob",
                id="message-id-4",
                text="Bob's edited message",
                published_at="2022-06-04T19:10:00",
            ),
        )

    def test_user_cannot_edit_a_message_on_his_timeline_to_more_than_280_characters(
        self,
    ):
        text_with_more_than_280_characters = (
            "Lorem ipsum dolor sit amet, consectetur "
            "adipiscing elit. Cras mauris lacus, fringilla eu est vitae, varius "
            "viverra nisl. Pellentesque habitant morbi tristique senectus et netus "
            "et malesuada fames ac turpis egestas. Vivamus suscipit feugiat "
            "sollicitudin. Aliquam erat volutpat amet."
        )
        original_message = Message(
            author="Bob",
            id="message-id-4",
            text="Bob's last message",
            published_at="2022-06-04T19:02:20",
        )
        self.given_following_messages_exist([original_message])
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=10, second=0)
        )
        self.when_user_edits_message(
            EditMessageCommand(
                author="Bob",
                id="message-id-4",
                text=text_with_more_than_280_characters,
            )
        )
        self.then_editing_should_be_refused_with_error(
            expected_error=MessageTextTooLongError
        )
        self.then_message_should_be(original_message)

    """
    Rule: a message cannot be empty
    """

    def test_user_cannot_edit_a_message_on_his_timeline_to_an_empty_message(self):
        text_empty = ""
        original_message = Message(
            author="Bob",
            id="message-id-4",
            text="Bob's last message",
            published_at="2022-06-04T19:02:20",
        )
        self.given_following_messages_exist([original_message])
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=10, second=0)
        )
        self.when_user_edits_message(
            EditMessageCommand(
                author="Bob",
                id="message-id-4",
                text=text_empty,
            )
        )
        self.then_editing_should_be_refused_with_error(
            expected_error=MessageTextEmptyError
        )
        self.then_message_should_be(original_message)

    def test_user_cannot_edit_a_message_on_his_timeline_to_only_space_characters(
        self,
    ):
        text_with_only_space_characters = "      "
        original_message = Message(
            author="Bob",
            id="message-id-4",
            text="Bob's last message",
            published_at="2022-06-04T19:02:20",
        )
        self.given_following_messages_exist([original_message])
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=10, second=0)
        )
        self.when_user_edits_message(
            EditMessageCommand(
                author="Bob",
                id="message-id-4",
                text=text_with_only_space_characters,
            )
        )
        self.then_editing_should_be_refused_with_error(
            expected_error=MessageTextEmptyError
        )
        self.then_message_should_be(original_message)
