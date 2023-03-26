from datetime import datetime

from src.application.ports.followee_repository import IFolloweeRepository
from src.application.ports.message_repository import IMessageRepository
from src.application.use_cases.view_wall_use_case import ViewWallUseCase
from src.infrastructure.adapters.stub_date_time_provider import StubDateTimeProvider


class WallFixture:
    def __init__(
        self,
        message_repository: IMessageRepository,
        followee_repository: IFolloweeRepository,
    ):
        self.message_repository = message_repository
        self.followee_repository = followee_repository
        self.date_time_provider = StubDateTimeProvider()

    # GIVEN
    # =====
    def given_now_is(self, date_time: datetime):
        self.date_time_provider.now = date_time

    # WHEN
    # ====
    def when_user_wants_to_see_his_wall(self, user: str):
        view_wall_use_case = ViewWallUseCase(
            message_repository=self.message_repository,
            followee_repository=self.followee_repository,
            date_time_provider=self.date_time_provider,
        )
        self.wall = view_wall_use_case.handle(user=user)

    # THEN
    # ====
    def then_user_should_see_on_his_wall(self, expected_wall):
        assert self.wall == expected_wall
