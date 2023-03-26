import itertools

from src.application.ports.datetime_provider import IDateTimeProvider
from src.application.ports.followee_repository import IFolloweeRepository
from src.application.ports.message_repository import IMessageRepository
from src.domain.timeline import Timeline


class ViewWallUseCase:
    def __init__(
        self,
        message_repository: IMessageRepository,
        followee_repository: IFolloweeRepository,
        date_time_provider: IDateTimeProvider,
    ):
        self.message_repository = message_repository
        self.followee_repository = followee_repository
        self.date_time_provider = date_time_provider

    def handle(self, user: str):
        users = [user, *self.followee_repository.list_followees_of_user(user=user)]
        messages = list(
            itertools.chain.from_iterable(
                self.message_repository.list_messages_by_author(author=user)
                for user in users
            )
        )
        timeline = Timeline(messages=messages, now=self.date_time_provider.get_now())
        return timeline.get_content()
