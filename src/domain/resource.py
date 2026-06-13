from dataclasses import dataclass


@dataclass(frozen=True)
class Resource:
    id: str
    name: str
