from dataclasses import dataclass


@dataclass
class User:
    name: str
    surname: str
    password: str
    id: int
