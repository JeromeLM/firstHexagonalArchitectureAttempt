import argparse
import random

from src.application.use_cases.follow_user_use_case import FollowUserCommand, \
    FollowUserUseCase
from src.infrastructure.adapters.file_system_followee_repository import \
    FileSystemFolloweeRepository
from src.infrastructure.adapters.file_system_message_repository import (
    FileSystemMessageRepository,
)
from src.application.use_cases.post_message_use_case import (
    PostMessageCommand,
    PostMessageUseCase,
)
from src.application.use_cases.edit_message_use_case import (
    EditMessageCommand,
    EditMessageUseCase,
)
from src.application.use_cases.view_timeline_use_case import ViewTimelineUseCase
from src.infrastructure.adapters.real_date_time_provider import RealDateTimeProvider

# TODO jlm: This file is intentionally quick and dirty driven !

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "-c",
    "--command",
    help="the command to execute ('post' or 'view' or 'edit')",
    required=True,
)
arg_parser.add_argument(
    "-u", "--user", help="the user initiating the command", required=True
)
arg_parser.add_argument("-m", "--message", help="the message", required=False)
arg_parser.add_argument("-i", "--id", help="the message id", required=False)
arg_parser.add_argument("-f", "--followee", help="the user to follow", required=False)

args = arg_parser.parse_args()
print(f"args = {args}")

message_repository = FileSystemMessageRepository()
date_time_provider = RealDateTimeProvider()
followee_repository = FileSystemFolloweeRepository()

match args.command:
    case "post":
        msg_id = str(random.randint(1, 1000))
        post_message_command = PostMessageCommand(
            id=msg_id, text=args.message, author=args.user
        )
        print(post_message_command)
        try:
            post_message_use_case = PostMessageUseCase(
                message_repository, date_time_provider
            )
            post_message_use_case.handle(post_message_command)
            print(f"\nMessage posted ! \n{message_repository.get_by_id(msg_id)}")
        except Exception as e:
            print(e)
    case "view":
        author = args.user
        try:
            view_timeline_use_case = ViewTimelineUseCase(
                message_repository, date_time_provider
            )
            timeline = view_timeline_use_case.handle(author)
            print(f"\nTimeline of {author} : \n{timeline}")
        except Exception as e:
            print(e)
    case "edit":
        msg_id = args.id
        edit_message_command = EditMessageCommand(
            id=msg_id, text=args.message, author=args.user
        )
        print(edit_message_command)
        try:
            edit_message_use_case = EditMessageUseCase(
                message_repository, date_time_provider
            )
            edit_message_use_case.handle(edit_message_command)
            print(f"\nMessage edited ! \n{message_repository.get_by_id(msg_id)}")
        except Exception as e:
            print(e)
    case "follow":
        user = args.user
        followee = args.followee
        follow_user_command = FollowUserCommand(user=user, user_to_follow=followee)
        try:
            follow_user_use_case = FollowUserUseCase(followee_repository)
            follow_user_use_case.handle(follow_user_command)
            print(f"\nUser followed ! \n{followee_repository.list_followees_of_user(user)}")
        except Exception as e:
            print(e)
    case _:
        print(f"Unsupported command '{args.command}'")
