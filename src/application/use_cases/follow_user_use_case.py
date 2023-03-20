from dataclasses import dataclass

from src.application.ports.followee_repository import IFolloweeRepository
from src.domain.followee import Followee


@dataclass
class FollowUserCommand:
    user: str
    user_to_follow: str


class FollowUserUseCase:
    def __init__(self, followee_repository: IFolloweeRepository):
        self.followee_repository = followee_repository

    def handle(self, follow_user_command: FollowUserCommand):
        followee = Followee(
            user=follow_user_command.user, followee=follow_user_command.user_to_follow
        )
        self.followee_repository.save(followee)
