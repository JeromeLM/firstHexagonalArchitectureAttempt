import json
import os
from unittest import TestCase

from src.domain.followee import Followee
from src.infrastructure.adapters.file_system_followee_repository import (
    FileSystemFolloweeRepository,
)


class TestFileSystemFolloweeRepository(TestCase):
    followees_test_filepath = os.path.join(
        os.path.dirname(__file__), "fs_followee_repository_test.json"
    )

    def setUp(self) -> None:
        if os.path.exists(self.followees_test_filepath):
            os.remove(self.followees_test_filepath)
        with open(self.followees_test_filepath, "w") as f:
            json.dump({}, f)
        self.followee_repository = FileSystemFolloweeRepository(
            filepath=self.followees_test_filepath
        )

    def test_can_save_a_followee_in_the_filesystem(self):
        self.followee_repository.save(Followee(user="Bob", followee="David"))
        with open(self.followees_test_filepath, "r") as f:
            followees = json.load(f)
        assert followees["Bob"] == ["David"]

    def test_can_list_followees_of_a_user(self):
        with open(self.followees_test_filepath, "w") as f:
            f.write(
                json.dumps(
                    {"Kevin": ["Salma", "George"], "Bob": ["Jane", "David"]},
                )
            )
        followees = self.followee_repository.list_followees_of_user("Bob")
        assert followees == ["Jane", "David"]

    def test_can_add_a_followee_to_a_user_in_the_filesystem(self):
        with open(self.followees_test_filepath, "w") as f:
            f.write(
                json.dumps(
                    {"Kevin": ["Salma", "George"], "Bob": ["Jane", "David"]},
                )
            )
        self.followee_repository.save(Followee(user="Bob", followee="Franck"))
        with open(self.followees_test_filepath, "r") as f:
            file_content = json.load(f)
        assert file_content == {
            "Kevin": ["Salma", "George"],
            "Bob": ["Jane", "David", "Franck"],
        }
