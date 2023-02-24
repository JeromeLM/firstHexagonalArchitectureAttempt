from datetime import datetime
from unittest import TestCase

from src.post_message_use_case import (
    PostMessageUseCase,
    Message,
    PostMessageCommand,
    IMessageRepository,
    IDateTimeProvider,
    MessageTextTooLongError,
    MessageTextEmptyError,
)


class InMemoryMessageRepository(IMessageRepository):
    def save(self, msg: Message):
        self.message = msg

    def get(self) -> Message:
        return self.message


class StubDateTimeProvider(IDateTimeProvider):
    now: datetime

    def get_now(self) -> str:
        return self.now.isoformat()


class TestPostingMessage(TestCase):
    thrown_error = None
    message_repository = InMemoryMessageRepository()
    date_time_provider = StubDateTimeProvider()

    """
    Rule: a message must have a max length of 280 characters
    """

    def test_user_can_post_a_message_on_his_timeline(self):
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=0, second=0)
        )
        self.when_user_posts_a_message(
            PostMessageCommand(id="message-id", text="Hello everyone", author="Bob")
        )
        self.then_posted_message_should_be(
            Message(
                id="message-id",
                text="Hello everyone",
                author="Bob",
                published_at="2022-06-04T19:00:00",
            )
        )

    def test_user_cannot_post_a_message_on_his_timeline_with_more_than_280_characters(
        self,
    ):
        text_with_more_than_280_characters = (
            "Lorem ipsum dolor sit amet, consectetur "
            "adipiscing elit. Cras mauris lacus, fringilla eu est vitae, varius "
            "viverra nisl. Pellentesque habitant morbi tristique senectus et netus "
            "et malesuada fames ac turpis egestas. Vivamus suscipit feugiat "
            "sollicitudin. Aliquam erat volutpat amet."
        )
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=0, second=0)
        )
        self.when_user_posts_a_message(
            PostMessageCommand(
                id="message-id", text=text_with_more_than_280_characters, author="Bob"
            )
        )
        self.then_posting_should_be_refused_with_error(MessageTextTooLongError)

    """
    Rule: a message cannot be empty
    """

    def test_user_cannot_post_an_empty_message_on_his_timeline(self):
        text_empty = ""
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=0, second=0)
        )
        self.when_user_posts_a_message(
            PostMessageCommand(id="message-id", text=text_empty, author="Bob")
        )
        self.then_posting_should_be_refused_with_error(MessageTextEmptyError)

    def test_user_cannot_post_a_message_on_his_timeline_with_only_space_characters(
        self,
    ):
        text_with_only_space_characters = "      "
        self.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=0, second=0)
        )
        self.when_user_posts_a_message(
            PostMessageCommand(
                id="message-id", text=text_with_only_space_characters, author="Bob"
            )
        )
        self.then_posting_should_be_refused_with_error(MessageTextEmptyError)

    """
    Helpers
    """

    @classmethod
    def given_now_is(cls, date_time: datetime):
        cls.date_time_provider.now = date_time

    @classmethod
    def when_user_posts_a_message(cls, message_command: PostMessageCommand):
        try:
            postMessageUseCase = PostMessageUseCase(
                cls.message_repository, cls.date_time_provider
            )
            postMessageUseCase.handle(message_command)
        except Exception as e:
            cls.thrown_error = e

    @classmethod
    def then_posted_message_should_be(cls, expected_message: Message):
        assert cls.message_repository.get() == expected_message

    @classmethod
    def then_posting_should_be_refused_with_error(
        cls, expected_error: [MessageTextTooLongError, MessageTextEmptyError]
    ):
        assert isinstance(cls.thrown_error, expected_error)
