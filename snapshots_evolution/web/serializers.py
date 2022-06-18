from typing import Any

from pydantic import BaseModel


class CalculateObjectsEvolutionsRequest(BaseModel):
    snapshots: list[dict]
    key_field_name: str
    datetime_field_name: str
    exclude_fields_names: list[str]


class DiffResponse(BaseModel):
    field_name: str
    value_old: Any
    value_new: Any


class EvolutionResponse(BaseModel):
    datetime: Any
    diffs: list[DiffResponse]
    snapshot: dict


class ObjectEvolutionsResponse(BaseModel):
    key: str
    datetime: Any
    snapshot_initial: dict
    evolutions: list[EvolutionResponse]
