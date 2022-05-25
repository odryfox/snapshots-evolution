from collections import defaultdict
from dataclasses import dataclass
from typing import List

from domain.entities import ObjectEvolutions, Evolution, Diff


@dataclass(frozen=True)
class SnapshotsGroupDTO:
    key: str
    snapshots: list[dict]


class CalculateObjectsEvolutionsService:

    def execute(
        self,
        snapshots: List[dict],
        key_field_name: str,
        datetime_field_name: str,
        exclude_fields_names: List[str],
    ) -> List[ObjectEvolutions]:

        snapshots_filtered = self._filter_snapshots_by_required_fields_names(
            snapshots=snapshots,
            required_fields_names=[key_field_name, datetime_field_name],
        )

        snapshots_groups_dtos = self._group_snapshots_by_key(
            snapshots=snapshots_filtered,
            key_field_name=key_field_name,
        )

        objects_evolutions = self._calculate_objects_evolutions(
            snapshots_groups_dtos=snapshots_groups_dtos,
            datetime_field_name=datetime_field_name,
            exclude_fields_names=exclude_fields_names,
        )

        return objects_evolutions

    def _filter_snapshots_by_required_fields_names(
        self,
        snapshots: list[dict],
        required_fields_names: list[str],
    ) -> list[dict]:
        snapshots_filtered = snapshots
        for required_field_name in required_fields_names:
            snapshots_filtered = [
                s for s in snapshots_filtered
                if required_field_name in s
            ]
        return snapshots_filtered

    def _group_snapshots_by_key(
        self,
        snapshots: list[dict],
        key_field_name: str,
    ) -> list[SnapshotsGroupDTO]:

        snapshots_groups_by_key_map = defaultdict(list)

        for snapshot in snapshots:
            key = snapshot[key_field_name]
            snapshots_groups_by_key_map[key].append(snapshot)

        snapshots_groups_dtos = [
            SnapshotsGroupDTO(
                key=key,
                snapshots=snapshots,
            )
            for key, snapshots in snapshots_groups_by_key_map.items()
        ]
        return snapshots_groups_dtos

    def _calculate_objects_evolutions(
        self,
        snapshots_groups_dtos: list[SnapshotsGroupDTO],
        datetime_field_name: str,
        exclude_fields_names: list[str],
    ) -> list[ObjectEvolutions]:

        exclude_fields_names_set = set(exclude_fields_names + [datetime_field_name])

        objects_evolutions = []

        for snapshots_group_dto in snapshots_groups_dtos:
            object_key = snapshots_group_dto.key
            snapshots_sorted = self._sort_snapshots_by_field_name(
                snapshots=snapshots_group_dto.snapshots,
                field_name=datetime_field_name,
            )
            snapshot_initial = snapshots_sorted[0]
            snapshots_other = snapshots_sorted[1:]

            evolutions = self._calculate_object_evolutions(
                snapshot_initial=snapshot_initial,
                snapshots_other=snapshots_other,
                datetime_field_name=datetime_field_name,
                exclude_fields_names_set=exclude_fields_names_set,
            )

            objects_evolutions.append(
                ObjectEvolutions(
                    key=object_key,
                    datetime=snapshot_initial[datetime_field_name],
                    snapshot_initial=snapshot_initial,
                    evolutions=evolutions,
                )
            )

        return objects_evolutions

    def _sort_snapshots_by_field_name(
        self,
        snapshots: list[dict],
        field_name: str,
    ) -> list[dict]:
        return sorted(snapshots, key=lambda i: i[field_name])

    def _calculate_object_evolutions(
        self,
        snapshot_initial: dict,
        snapshots_other: list[dict],
        datetime_field_name: str,
        exclude_fields_names_set: set[str],
    ) -> list[Evolution]:
        evolutions = []
        snapshot_prev = snapshot_initial
        for snapshot_current in snapshots_other:
            diffs = self._calculate_diffs(
                snapshot_prev=snapshot_prev,
                snapshot_current=snapshot_current,
                exclude_fields_names_set=exclude_fields_names_set,
            )

            evolutions.append(
                Evolution(
                    datetime=snapshot_current[datetime_field_name],
                    diffs=diffs,
                    snapshot=snapshot_current,
                )
            )

            snapshot_prev = snapshot_current

        return evolutions

    def _calculate_diffs(
        self,
        snapshot_prev: dict,
        snapshot_current: dict,
        exclude_fields_names_set: set[str],
    ) -> list[Diff]:

        diffs = []

        for field_name, value in snapshot_current.items():
            if field_name in exclude_fields_names_set:
                continue

            value_old = snapshot_prev.get(field_name)
            if value == value_old:
                continue

            diffs.append(
                Diff(
                    field_name=field_name,
                    value_old=value_old,
                    value_new=value,
                )
            )

        return diffs
