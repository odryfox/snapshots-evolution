from fastapi.testclient import TestClient

from web.app import app

client = TestClient(app)


def test_get():
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'res': []}
