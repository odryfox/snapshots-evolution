from dataclasses import asdict
from typing import Type, TypeVar, Any, Iterable

from pydantic import parse_obj_as

T = TypeVar('T')


def parse_dataclass_as(type_: Type[T], obj: Any) -> T:
    if isinstance(obj, Iterable):
        obj_dict = [asdict(o) for o in obj]
    else:
        obj_dict = asdict(obj)

    return parse_obj_as(type_, obj_dict)
