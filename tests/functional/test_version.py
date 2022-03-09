from tests import BASE_API


def test_version(client):
    response = client.get(f'{BASE_API}/version')
    assert response.status_code == 200
