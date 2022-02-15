import uuid

from _pytest.recwarn import warns

from tests import BASE_API, OK, EMPTY_BODY, NOT_FOUND

users = {
    '1':
        [
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
subscription_id = ''


def test_retrieve_all_subscriptions_when_missing_subscriptions_return_empty_list(client):
    response = client.get(f'{BASE_API}/users/subscriptions')
    assert response.status_code == OK
    assert response.json == []


def test_create_subscription_with_empty_body_return_400_error(client):
    response = client.post(f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions')

    assert response.status_code == EMPTY_BODY
    assert response.json == {'error': 'Empty body'}


def test_create_subscription_with_body_return_created_subscription(client):

    response = client.post(f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions', json=users.get('1')[0])

    response_body = response.json
    del response_body['id']

    assert response.status_code == OK
    assert response_body == users.get('1')[0]


def test_retrieve_all_subscriptions_return_user_lists(client):
    response = client.get(f'{BASE_API}/users/subscriptions')

    response_body = response.json
    for user_subs in response_body:
        for subscription in user_subs.get('subscriptions'):
            del subscription['id']

    assert response.status_code == OK
    current_user = list(users.keys())[0]
    assert response_body == \
           [
               {
                   "user_id": current_user,
                   "subscriptions":
                       [

                           users.get('1')[0]

                       ]
               }
           ]


def test_retrieve_missing_subscription_return_404_error(client):
    response = client.get(f'/users/{list(users.keys())[0]}/subscriptions/{uuid.uuid4().__str__()}')
    assert response.status_code == 404


def test_retrieve_subscription_return_object(client):
    global subscription_id
    # get all user subscriptions
    path = f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions'
    response = client.get(path)
    assert response.status_code == OK
    # get a subscription ID.
    subscription_id = response.json[0].get('id')
    # get that subscription
    response = client.get(f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions/{subscription_id}')
    assert response.status_code == OK
    response_content = response.json
    del response_content['id']
    assert response_content == users.get('1')[0]


def test_get_user_list_category_dont_exist_404_error(client):
    unexisting_category = 'category3'
    response = client.get(f'{BASE_API}/users/subscriptions/{unexisting_category}')
    assert response.status_code == NOT_FOUND


def test_get_user_list_category_exist(client):
    response = client.get(f'{BASE_API}/users/subscriptions/{users.get("1")[0].get("category")}')
    assert response.status_code == OK
    # assert response.json.get('users')[0] == list(users.keys())[0]
    assert response.json == {"users": [list(users.keys())[0]]}


def test_activate_subscription_dont_exist_404_error(client):
    response = client.patch(f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions/{subscription_id}{1}/activate')
    assert response.status_code == NOT_FOUND


def test_activate_subscription_exist(client):
    response = client.patch(f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions/{subscription_id}/activate')
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    assert response_body == users.get('1')[0]


def test_deactivate_subscription_dont_exist_404_error(client):
    response = client.patch(f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions/{subscription_id}{1}/deactivate')
    assert response.status_code == NOT_FOUND


def test_deactivate_subscription_exist(client):
    response = client.patch(f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions/{subscription_id}/deactivate')
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    inverted_bool = users.get('1')[0]
    inverted_bool['active'] = not inverted_bool.get('active')
    assert response_body == inverted_bool


def test_delete_subscription_dont_exist_404_error(client):
    response = client.delete(f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions/{subscription_id}{1}')
    assert response.status_code == NOT_FOUND


def test_delete_subscription_exist(client):
    response = client.delete(f'{BASE_API}/users/{list(users.keys())[0]}/subscriptions/{subscription_id}')
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    assert response_body == users.get('1')[0]


print(warns)
