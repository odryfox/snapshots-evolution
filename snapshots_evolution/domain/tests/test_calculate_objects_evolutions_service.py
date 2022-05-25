from domain.calculate_objects_evolutions_service import (
    CalculateObjectsEvolutionsService,
)


class TestCalculateObjectsEvolutionsService:

    def setup_method(self):
        self.service = CalculateObjectsEvolutionsService()

    def test__few_objects(self):
        snapshots = [
            {'object_id': 1, 'date': '2022-07-10', 'name': 'John', 'age': 25},
            {'object_id': 2, 'date': '2022-07-11', 'name': 'Mark', 'age': 26},
            {'object_id': 1, 'date': '2022-07-12', 'name': 'John Doe', 'age': 26},
            {'object_id': 2, 'date': '2022-07-13', 'name': 'Mark', 'age': 26},
        ]

        objects_evolutions = self.service.execute(
            snapshots=snapshots,
            key_field_name='object_id',
            datetime_field_name='date',
            exclude_fields_names=[],
        )

        assert len(objects_evolutions) == 2

        object_evolutions = objects_evolutions[0]
        assert object_evolutions.key == 1
        assert object_evolutions.datetime == '2022-07-10'
        assert object_evolutions.snapshot_initial == snapshots[0]
        assert len(object_evolutions.evolutions) == 1

        evolution = object_evolutions.evolutions[0]
        assert evolution.datetime == '2022-07-12'
        assert evolution.snapshot == snapshots[2]
        assert len(evolution.diffs) == 2

        diff = evolution.diffs[0]
        assert diff.field_name == 'name'
        assert diff.value_old == 'John'
        assert diff.value_new == 'John Doe'

        diff = evolution.diffs[1]
        assert diff.field_name == 'age'
        assert diff.value_old == 25
        assert diff.value_new == 26

        object_evolutions = objects_evolutions[1]
        assert object_evolutions.key == 2
        assert object_evolutions.datetime == '2022-07-11'
        assert object_evolutions.snapshot_initial == snapshots[1]
        assert len(object_evolutions.evolutions) == 1

        evolution = object_evolutions.evolutions[0]
        assert evolution.datetime == '2022-07-13'
        assert evolution.snapshot == snapshots[3]
        assert len(evolution.diffs) == 0

    def test__no_snapshots(self):
        snapshots = []

        objects_evolutions = self.service.execute(
            snapshots=snapshots,
            key_field_name='object_id',
            datetime_field_name='date',
            exclude_fields_names=[],
        )

        assert len(objects_evolutions) == 0

    def test__exclude_field(self):
        snapshots = [
            {'object_id': 1, 'date': '2022-07-10', 'age': 25, 'name': 'John'},
            {'object_id': 1, 'date': '2022-07-12', 'age': 26, 'name': 'John Doe'},
        ]

        objects_evolutions = self.service.execute(
            snapshots=snapshots,
            key_field_name='object_id',
            datetime_field_name='date',
            exclude_fields_names=['name'],
        )

        assert len(objects_evolutions) == 1

        object_evolutions = objects_evolutions[0]
        assert object_evolutions.key == 1
        assert object_evolutions.datetime == '2022-07-10'
        assert object_evolutions.snapshot_initial == snapshots[0]
        assert len(object_evolutions.evolutions) == 1

        evolution = object_evolutions.evolutions[0]
        assert evolution.datetime == '2022-07-12'
        assert evolution.snapshot == snapshots[1]
        assert len(evolution.diffs) == 1

        diff = evolution.diffs[0]
        assert diff.field_name == 'age'
        assert diff.value_old == 25
        assert diff.value_new == 26

    def test__no_key_field_in_snapshot(self):
        snapshots = [
            {'id': 1, 'date': '2022-07-10', 'age': 25},
            {'object_id': 1, 'date': '2022-07-12', 'age': 26},
        ]

        objects_evolutions = self.service.execute(
            snapshots=snapshots,
            key_field_name='object_id',
            datetime_field_name='date',
            exclude_fields_names=[],
        )

        assert len(objects_evolutions) == 1

        object_evolutions = objects_evolutions[0]
        assert object_evolutions.key == 1
        assert object_evolutions.datetime == '2022-07-12'
        assert object_evolutions.snapshot_initial == snapshots[1]
        assert len(object_evolutions.evolutions) == 0

    def test__no_datetime_field_in_snapshot(self):
        snapshots = [
            {'object_id': 1, 'd': '2022-07-10', 'age': 25},
            {'object_id': 1, 'date': '2022-07-12', 'age': 26},
        ]

        objects_evolutions = self.service.execute(
            snapshots=snapshots,
            key_field_name='object_id',
            datetime_field_name='date',
            exclude_fields_names=[],
        )

        assert len(objects_evolutions) == 1

        object_evolutions = objects_evolutions[0]
        assert object_evolutions.key == 1
        assert object_evolutions.datetime == '2022-07-12'
        assert object_evolutions.snapshot_initial == snapshots[1]
        assert len(object_evolutions.evolutions) == 0

    def test__no_exclude_field_in_snapshot(self):
        snapshots = [
            {'object_id': 1, 'date': '2022-07-10', 'age': 25},
            {'object_id': 1, 'date': '2022-07-12', 'age': 26, 'name': 'John Doe'},
        ]

        objects_evolutions = self.service.execute(
            snapshots=snapshots,
            key_field_name='object_id',
            datetime_field_name='date',
            exclude_fields_names=['name'],
        )

        assert len(objects_evolutions) == 1

        object_evolutions = objects_evolutions[0]
        assert object_evolutions.key == 1
        assert object_evolutions.datetime == '2022-07-10'
        assert object_evolutions.snapshot_initial == snapshots[0]
        assert len(object_evolutions.evolutions) == 1

        evolution = object_evolutions.evolutions[0]
        assert evolution.datetime == '2022-07-12'
        assert evolution.snapshot == snapshots[1]
        assert len(evolution.diffs) == 1

        diff = evolution.diffs[0]
        assert diff.field_name == 'age'
        assert diff.value_old == 25
        assert diff.value_new == 26

    def test__no_field_in_one_but_exists_in_other_snapshot(self):
        snapshots = [
            {'object_id': 1, 'date': '2022-07-10'},
            {'object_id': 1, 'date': '2022-07-12', 'age': 26},
        ]

        objects_evolutions = self.service.execute(
            snapshots=snapshots,
            key_field_name='object_id',
            datetime_field_name='date',
            exclude_fields_names=[],
        )

        assert len(objects_evolutions) == 1

        object_evolutions = objects_evolutions[0]
        assert object_evolutions.key == 1
        assert object_evolutions.datetime == '2022-07-10'
        assert object_evolutions.snapshot_initial == snapshots[0]
        assert len(object_evolutions.evolutions) == 1

        evolution = object_evolutions.evolutions[0]
        assert evolution.datetime == '2022-07-12'
        assert evolution.snapshot == snapshots[1]
        assert len(evolution.diffs) == 1

        diff = evolution.diffs[0]
        assert diff.field_name == 'age'
        assert diff.value_old is None
        assert diff.value_new == 26

    def test__exclude_field_is_key_field(self):
        snapshots = [
            {'object_id': 1, 'date': '2022-07-10', 'age': 25},
            {'object_id': 1, 'date': '2022-07-12', 'age': 26},
        ]

        objects_evolutions = self.service.execute(
            snapshots=snapshots,
            key_field_name='object_id',
            datetime_field_name='date',
            exclude_fields_names=['object_id'],
        )

        assert len(objects_evolutions) == 1

        object_evolutions = objects_evolutions[0]
        assert object_evolutions.key == 1
        assert object_evolutions.datetime == '2022-07-10'
        assert object_evolutions.snapshot_initial == snapshots[0]
        assert len(object_evolutions.evolutions) == 1

        evolution = object_evolutions.evolutions[0]
        assert evolution.datetime == '2022-07-12'
        assert evolution.snapshot == snapshots[1]
        assert len(evolution.diffs) == 1

        diff = evolution.diffs[0]
        assert diff.field_name == 'age'
        assert diff.value_old == 25
        assert diff.value_new == 26
