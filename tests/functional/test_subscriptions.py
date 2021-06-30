import json
import uuid

users = ['user1', 'user2']
subscriptions = [
    {
        "category": "category1",
    },
    {
        "category": "category2",
    }
]


def test_create_subscription_with_empty_body_return_400_error(client):
    response = client.post(f'/users/{users[0]}/subscriptions')

    assert response.status_code == 400
    assert response.json == {'error': 'Empty body'}


def test_(client):
    response = client.post(f'/users/{users[0]}/subscriptions', json=subscriptions[0])

    assert response.status_code == 200
    assert response.json == {'error': 'Empty body'}
