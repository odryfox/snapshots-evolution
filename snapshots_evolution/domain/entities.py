from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Diff:
    field_name: str
    value_old: Any
    value_new: Any


@dataclass(frozen=True)
class Evolution:
    datetime: Any
    diffs: list[Diff]
    snapshot: dict


@dataclass(frozen=True)
class ObjectEvolutions:
    key: str
    datetime: Any
    snapshot_initial: dict
    evolutions: list[Evolution]
