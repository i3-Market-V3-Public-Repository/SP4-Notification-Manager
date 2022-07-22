import uuid
from tests import BASE_API, OK_CODE, BODY_ERROR_CODE, NOT_FOUND_CODE, ALREADY_EXIST_BODY, \
    NOT_FOUND_BODY
from copy import deepcopy
user_id = '1'
user_subscriptions = [{"category": "category1"}, {"category": "category2"}]

user_subscription_output = deepcopy(user_subscriptions)
# noinspection PyTypeChecker
user_subscription_output[0]['active'] = True
# noinspection PyTypeChecker
user_subscription_output[1]['active'] = False

subscription_id = ''


def test_retrieve_all_subscriptions_when_missing_subscriptions_return_empty_list(client):
    response = client.get(f'{BASE_API}/users/subscriptions')
    assert response.status_code == OK_CODE
    assert response.json == []


def test_create_subscription_with_empty_body_return_400_error_no_body(client):
    response = client.post(f'{BASE_API}/users/{user_id}/subscriptions')

    assert response.status_code == BODY_ERROR_CODE
    assert response.json == {'detail': {'json': {'category': ['Missing data for required field.']}},
                             'message': 'Validation error'} != {}


def test_create_subscription_with_empty_body_return_400_error_incomplete(client):
    response = client.post(f'{BASE_API}/users/{user_id}/subscriptions', json={"a": "b"})

    assert response.status_code == BODY_ERROR_CODE
    assert response.json == {'detail': {'json': {'a': ['Unknown field.'],
                                                 'category': ['Missing data for required field.']}},
                             'message': 'Validation error'}


def test_create_subscription_with_body_return_created_subscription(client):
    response = client.post(f'{BASE_API}/users/{user_id}/subscriptions', json=user_subscriptions[0])

    response_body = response.json
    if response_body.get('id'):
        del response_body['id']
    else:
        raise Exception(f"Error in request: sent:{user_subscriptions[0]}\nresponse:{response.json}")
    assert response.status_code == OK_CODE
    assert response_body == user_subscription_output[0]


def test_create_subscription_with_body_return_created_subscription_400_already_exist(client):
    response = client.post(f'{BASE_API}/users/{user_id}/subscriptions', json=user_subscriptions[0])
    assert response.status_code == BODY_ERROR_CODE
    # assert response.json == {'error': 'Already exists subscription to category'}
    assert response.json == ALREADY_EXIST_BODY


def test_retrieve_all_subscriptions_return_user_lists(client):
    response = client.get(f'{BASE_API}/users/subscriptions')

    response_body = response.json
    for user_subs in response_body:
        for subscription in user_subs.get('subscriptions'):
            del subscription['id']

    assert response.status_code == OK_CODE
    current_user = user_id
    assert response_body == \
           [
               {
                   "user_id": current_user,
                   "subscriptions":
                       [
                           user_subscription_output[0]
                       ]
               }
           ]


def test_retrieve_missing_subscription_return_404_error_sub_not_found(client):
    response = client.get(f'{BASE_API}/users/{user_id}/subscriptions/{uuid.uuid4().__str__()}')
    assert response.status_code == 404
    assert response.json == NOT_FOUND_BODY


def test_retrieve_missing_subscription_return_404_error_user_not_found(client):
    response = client.get(f'{BASE_API}/users/a/subscriptions')
    assert response.status_code == 404
    assert response.json == NOT_FOUND_BODY


def test_retrieve_subscription_return_object(client):
    global subscription_id
    # get all user subscriptions
    path = f'{BASE_API}/users/{user_id}/subscriptions'
    response = client.get(path)
    assert response.status_code == OK_CODE
    # get a subscription ID.
    subscription_id = response.json[0].get('id')
    # get that subscription
    response = client.get(f'{BASE_API}/users/{user_id}/subscriptions/{subscription_id}')
    assert response.status_code == OK_CODE
    response_content = response.json
    del response_content['id']
    assert response_content == user_subscription_output[0]


def test_get_user_list_category_dont_exist_404_error(client):
    unexisting_category = 'null'
    response = client.get(f'{BASE_API}/users/subscriptions/{unexisting_category}')
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_get_user_list_category_exist(client):
    response = client.get(f'{BASE_API}/users/subscriptions/{user_subscriptions[0].get("category")}')
    assert response.status_code == OK_CODE
    # assert response.json.get('users')[0] == user_id
    assert response.json == {"users": [user_id]}


def test_activate_subscription_dont_exist_404_error(client):
    response = client.patch(f'{BASE_API}/users/{user_id}/subscriptions/{subscription_id}{1}/activate')
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_activate_subscription_exist(client):
    response = client.patch(f'{BASE_API}/users/{user_id}/subscriptions/{subscription_id}/activate')
    assert response.status_code == OK_CODE
    response_body = response.json
    del response_body['id']
    assert response_body == user_subscription_output[0]


def test_deactivate_subscription_dont_exist_404_error(client):
    response = client.patch(f'{BASE_API}/users/{user_id}/subscriptions/{subscription_id}{1}/deactivate')
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_deactivate_subscription_exist(client):
    response = client.patch(f'{BASE_API}/users/{user_id}/subscriptions/{subscription_id}/deactivate')
    assert response.status_code == OK_CODE
    response_body = response.json
    del response_body['id']
    inverted_bool = user_subscription_output[0]
    inverted_bool['active'] = not inverted_bool.get('active')
    assert response_body == inverted_bool


def test_delete_subscription_dont_exist_404_error(client):
    response = client.delete(f'{BASE_API}/users/{user_id}/subscriptions/{subscription_id}{1}')
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_delete_subscription_exist(client):
    response = client.delete(f'{BASE_API}/users/{user_id}/subscriptions/{subscription_id}')
    assert response.status_code == OK_CODE
    response_body = response.json
    del response_body['id']
    assert response_body == user_subscription_output[0]
