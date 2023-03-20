import json
import os
from typing import List

from src.application.ports.followee_repository import IFolloweeRepository
from src.domain.followee import Followee


class FileSystemFolloweeRepository(IFolloweeRepository):
    filepath = os.path.abspath("./followees.json")

    def __init__(self, filepath=None):
        if filepath:
            self.filepath = filepath

    def save(self, followee: Followee):
        self._add_followee(followee)

    def list_followees_of_user(self, user: str) -> List[str]:
        file_content = self._get_file_content()
        return file_content.get(user, [])

    def _add_followee(self, followee: Followee):
        file_content = self._get_file_content()
        existing_followees = file_content.get(followee.user, [])
        existing_followees.append(followee.followee)
        file_content[followee.user] = existing_followees
        with open(self.filepath, "w") as f:
            json.dump(file_content, f)

    def _get_file_content(self):
        with open(self.filepath, "r") as f:
            return json.load(f)
