from fastapi.testclient import TestClient

from web.app import app

client = TestClient(app)


def test_post():
    data = {
        'snapshots': [
            {'object_id': 1, 'date': '2022-07-10', 'name': 'John', 'age': 25},
            {'object_id': 2, 'date': '2022-07-11', 'name': 'Mark', 'age': 26},
            {'object_id': 1, 'date': '2022-07-12', 'name': 'John Doe', 'age': 26},
            {'object_id': 2, 'date': '2022-07-13', 'name': 'Mark', 'age': 26},
        ],
        'key_field_name': 'object_id',
        'datetime_field_name': 'date',
        'exclude_fields_names': [],
    }
    actual_response = client.post('/', json=data)

    expected_response = [
        {
            'key': '1',
            'datetime': '2022-07-10',
            'snapshot_initial': {
                'object_id': 1,
                'date': '2022-07-10',
                'name': 'John',
                'age': 25,
            },
            'evolutions': [
                {
                    'datetime': '2022-07-12',
                    'diffs': [
                        {
                            'field_name': 'name',
                            'value_old': 'John',
                            'value_new': 'John Doe',
                        },
                        {
                            'field_name': 'age',
                            'value_old': 25,
                            'value_new': 26,
                        },
                    ],
                    'snapshot': {
                        'object_id': 1,
                        'date': '2022-07-12',
                        'name': 'John Doe',
                        'age': 26,
                    },
                },
            ],
        },
        {
            'key': '2',
            'datetime': '2022-07-11',
            'snapshot_initial': {
                'object_id': 2,
                'date': '2022-07-11',
                'name': 'Mark',
                'age': 26,
            },
            'evolutions': [
                {
                    'datetime': '2022-07-13',
                    'diffs': [],
                    'snapshot': {
                        'object_id': 2,
                        'date': '2022-07-13',
                        'name': 'Mark',
                        'age': 26,
                    },
                },
            ],
        },
    ]
    assert actual_response.status_code == 200
    assert actual_response.json() == expected_response
