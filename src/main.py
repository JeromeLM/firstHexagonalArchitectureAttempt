import argparse
from datetime import datetime

from src.file_system_message_repository import FileSystemMessageRepository
from src.post_message_use_case import (
    PostMessageCommand,
    PostMessageUseCase,
    IDateTimeProvider,
)


class RealDateTimeProvider(IDateTimeProvider):
    def get_now(self):
        return datetime.now().isoformat()


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-c", "--command", help="the command to execute", required=True)
arg_parser.add_argument(
    "-u", "--user", help="the user initiating the command", required=True
)
arg_parser.add_argument("-m", "--message", help="the message", required=True)

args = arg_parser.parse_args()
print(f"args = {args}")

post_message_command = PostMessageCommand(
    id="the id", text=args.message, author=args.user
)
print(post_message_command)
message_repository = FileSystemMessageRepository()
date_time_provider = RealDateTimeProvider()

try:
    post_message_use_case = postMessageUseCase = PostMessageUseCase(
        message_repository, date_time_provider
    )
    postMessageUseCase.handle(post_message_command)
    print(f"\nMessage posted ! \n{message_repository.get()}")
except Exception as e:
    print(e)
