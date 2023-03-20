from dataclasses import dataclass


@dataclass
class Followee:
    user: str
    followee: str
