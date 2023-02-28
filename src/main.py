import argparse
import random
from datetime import datetime

from src.file_system_message_repository import FileSystemMessageRepository
from src.post_message_use_case import (
    PostMessageCommand,
    PostMessageUseCase,
    IDateTimeProvider,
)
from src.view_timeline_use_case import ViewTimelineUseCase


class RealDateTimeProvider(IDateTimeProvider):
    def get_now(self):
        return datetime.now().isoformat()


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "-c", "--command", help="the command to execute ('post' or 'view')", required=True
)
arg_parser.add_argument(
    "-u", "--user", help="the user initiating the command", required=True
)
arg_parser.add_argument("-m", "--message", help="the message", required=False)

args = arg_parser.parse_args()
print(f"args = {args}")

message_repository = FileSystemMessageRepository()
date_time_provider = RealDateTimeProvider()

if args.command == "post":
    msg_id = str(random.randint(1, 1000))
    post_message_command = PostMessageCommand(
        id=msg_id, text=args.message, author=args.user
    )
    print(post_message_command)
    try:
        post_message_use_case = postMessageUseCase = PostMessageUseCase(
            message_repository, date_time_provider
        )
        postMessageUseCase.handle(post_message_command)
        print(f"\nMessage posted ! \n{message_repository.get_by_id(msg_id)}")
    except Exception as e:
        print(e)
elif args.command == "view":
    author = args.user
    try:
        view_timeline_use_case = ViewTimelineUseCase(
            message_repository, date_time_provider
        )
        timeline = view_timeline_use_case.handle(author)
        print(f"\nTimeline of {author} : \n{timeline}")
    except Exception as e:
        print(e)
else:
    print(f"Unsupported command '{args.command}'")
