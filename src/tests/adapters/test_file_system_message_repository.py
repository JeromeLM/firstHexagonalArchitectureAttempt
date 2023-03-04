import json
import os
from unittest import TestCase

from src.infrastructure.adapters.file_system_message_repository import (
    FileSystemMessageRepository,
)
from src.tests.builders.message_builder import MessageBuilder


class TestFileSystemMessageRepository(TestCase):
    messages_test_filepath = os.path.join(
        os.path.dirname(__file__), "fs_message_repository_test.json"
    )

    def setUp(self) -> None:
        if os.path.exists(self.messages_test_filepath):
            os.remove(self.messages_test_filepath)
        with open(self.messages_test_filepath, "w") as f:
            json.dump([], f)

    def test_can_save_a_message_in_the_filesystem(self):
        message_repository = FileSystemMessageRepository(
            filepath=self.messages_test_filepath
        )
        message = (
            MessageBuilder()
            .with_id("message-id-1")
            .written_by("Bob")
            .with_text("Test save operation")
            .on("2022-06-04T19:00:00")
            .build()
        )
        message_repository.save(message)

        with open(self.messages_test_filepath, "r") as f:
            messages = json.load(f)
        assert messages == [
            {
                "id": "message-id-1",
                "author": "Bob",
                "text": "Test save operation",
                "published_at": "2022-06-04T19:00:00",
            }
        ]

    def test_can_edit_a_message_in_the_filesystem(self):
        message_repository = FileSystemMessageRepository(
            filepath=self.messages_test_filepath
        )
        with open(self.messages_test_filepath, "w") as f:
            json.dump(
                [
                    {
                        "id": "message-id-1",
                        "author": "Bob",
                        "text": "First message",
                        "published_at": "2022-06-04T19:00:00",
                    }
                ],
                f,
            )
        message = (
            MessageBuilder()
            .with_id("message-id-1")
            .written_by("Bob")
            .with_text("Test edit operation")
            .on("2022-06-04T19:05:00")
            .build()
        )
        message_repository.save(message)

        with open(self.messages_test_filepath, "r") as f:
            messages = json.load(f)
        assert messages == [
            {
                "id": "message-id-1",
                "author": "Bob",
                "text": "Test edit operation",
                "published_at": "2022-06-04T19:05:00",
            }
        ]

    def test_can_get_a_message_from_the_filesystem_by_its_id(self):
        message_repository = FileSystemMessageRepository(
            filepath=self.messages_test_filepath
        )
        with open(self.messages_test_filepath, "w") as f:
            json.dump(
                [
                    {
                        "id": "message-id-1",
                        "author": "Bob",
                        "text": "First message",
                        "published_at": "2022-06-04T19:00:00",
                    },
                    {
                        "id": "message-id-2",
                        "author": "Bob",
                        "text": "Test get message by its id",
                        "published_at": "2022-06-04T19:05:00",
                    },
                ],
                f,
            )
        message = message_repository.get_by_id("message-id-2")

        assert (
            message
            == MessageBuilder()
            .with_id("message-id-2")
            .written_by("Bob")
            .with_text("Test get message by its id")
            .on("2022-06-04T19:05:00")
            .build()
        )

    def test_can_get_all_messages_of_a_user_from_the_filesystem(self):
        message_repository = FileSystemMessageRepository(
            filepath=self.messages_test_filepath
        )
        with open(self.messages_test_filepath, "w") as f:
            json.dump(
                [
                    {
                        "id": "message-id-1",
                        "author": "Bob",
                        "text": "Test get all messages of user - 1",
                        "published_at": "2022-06-04T19:00:00",
                    },
                    {
                        "id": "message-id-2",
                        "author": "Jane",
                        "text": "Jane's message",
                        "published_at": "2022-06-04T19:05:00",
                    },
                    {
                        "id": "message-id-3",
                        "author": "Bob",
                        "text": "Test get all messages of user - 2",
                        "published_at": "2022-06-04T19:10:00",
                    },
                ],
                f,
            )
        messages = message_repository.list_messages_by_author("Bob")

        assert messages == [
            MessageBuilder()
            .with_id("message-id-1")
            .written_by("Bob")
            .with_text("Test get all messages of user - 1")
            .on("2022-06-04T19:00:00")
            .build(),
            MessageBuilder()
            .with_id("message-id-3")
            .written_by("Bob")
            .with_text("Test get all messages of user - 2")
            .on("2022-06-04T19:10:00")
            .build(),
        ]
