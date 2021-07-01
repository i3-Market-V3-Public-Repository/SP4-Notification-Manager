import json
import uuid

users = {
    '1': [
        {
            "category": "category1",
            "active": True
        },
        {
            "category": "category2",
            "active": False
        }
    ]
}


## TODO Testeado con postman, pendiente arreglar los tests

def test_retrieve_all_subscriptions_when_missing_subscriptions_return_empty_list(client):
    response = client.get(f'/users/subscriptions')

    assert response.status_code == 200
    assert response.json == {}


def test_create_subscription_with_empty_body_return_400_error(client):
    response = client.post(f'/users/{list(users.keys())[0]}/subscriptions')

    assert response.status_code == 400
    assert response.json == {'error': 'Empty body'}


def test_create_subscription_with_body_return_created_subscription(client):
    response = client.post(f'/users/{list(users.keys())[0]}/subscriptions', json=users.get('1')[0])

    response_body = response.json
    del response_body['id']

    assert response.status_code == 200
    assert response_body == users.get('1')[0]


def test_retrieve_all_subscriptions_return_user_lists(client):
    response = client.get(f'/users/subscriptions')

    response_body = response.json
    for subscription in response_body.get('1'):
        del subscription['id']

    assert response.status_code == 200
    assert response_body == {'1': [users.get('1')[0]]}


def test_retrieve_missing_subscription_return_404_error(client):
    response = client.get(f'/users/{list(users.keys())[0]}/subscriptions/{uuid.uuid4().__str__()}')

    assert response.status_code == 404


def test_retrieve_subscription_return_object(client):
    response = client.get(f'/users/{list(users.keys())[0]}/subscriptions/{users.get("1")[0].get("id")}')

    assert response.status_code == 200
    assert response.json == users.get("1")[0]
