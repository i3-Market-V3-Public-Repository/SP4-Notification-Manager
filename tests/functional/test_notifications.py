import uuid

import notification as notification
from _pytest.recwarn import warns

from tests import BASE_API, OK, BODY_ERROR, NOT_FOUND, EMPTY_BODY, INCOMPLETE_BODY, ALREADY_EXIST_BODY_SERVICE, \
    NOT_FOUND_BODY, QUEUE_ERROR, ALREADY_EXIST_BODY

output_notification = {'action': 'offering.new',
                       'data': {'category': 'Agriculture', 'msg': 'this is a new offering'},
                       'origin': 'string',
                       'receptor': 'UserID123',
                       'status': 'string',
                       'unread': True}
user_notifications = {
    '1':
        {
            "predefined": True,
            "message": {"msg": "this is a new offering", "category": "Agriculture"},
            "type": "offering.new",
            "status": "string",
            "receiver_id": "UserID123",
            "origin": "string"
        }
}

service_notifications = {
    '1':
        {
            "receiver_id": "offering.new",
            "message": {"msg": "this is a message!"}
        }
}

notification_id = ''


# RETURN ALL REGISTERED NOTIFICATIONS
def test_retrieve_all_notifications_return_empty_list(client):
    response = client.get(f'{BASE_API}/notification')
    assert response.status_code == OK
    assert response.json == []


def test_retrieve_all_unread_notifications_return_empty_list(client):
    response = client.get(f'{BASE_API}/notification/unread')
    assert response.status_code == OK
    assert response.json == []


# CREATE SERVICE NOTIFICATION
def test_create_notification_with_empty_body_return_400_error_no_body(client):
    response = client.post(f'{BASE_API}/notification/service')
    assert response.status_code == BODY_ERROR
    assert response.json == {'detail': {'json': {'receiver_id': ['Missing data for required field.']}},
                             'message': 'Validation error'}


# CREATE USER NOTIFICATION
def test_create_notification_with_empty_body_return_400_error_incomplete(client):
    body = {"a": "b"}
    response = client.post(f'{BASE_API}/notification/service', json=body)

    assert response.status_code == BODY_ERROR
    assert response.json == {'detail': {
        'json': {f'{list(body.keys())[0]}': ['Unknown field.'], 'receiver_id': ['Missing data for required field.']}},
                             'message': 'Validation error'}


def test_create_notification_with_body_return_created(client):
    global notification_id
    response = client.post(f'{BASE_API}/notification', json=user_notifications.get('1'))

    response_body = response.json
    notification_id = response_body.get('id')
    del response_body['id']

    assert response.status_code == OK
    assert response_body == output_notification


# RETRIEVE EXISTING USER NOTIFICATIONS
# def test_retrieve_all_notifications_return_notification_lists(client):
#    global notification_id
#    response = client.get(f'{BASE_API}/notification/user/{user_notifications.get("1").get("receiver_id")}')
#    response_body = response.json
#    del response_body['id']
#    assert response.status_code == OK
#    #assert response_body == output_notification


#  def test_retrieve_missing_notification_return_404_error_not_found(client):
#     response = client.get(f'{BASE_API}/notification/user/random')
#     assert response.status_code == 404
#     assert response.json == NOT_FOUND_BODY
#
#
# def test_retrieve_notification_by_id_return_object(client):
#    global notification_id
#    # get all registered services
#    path = f'{BASE_API}/notification'
#    response = client.get(path)
#    assert response.status_code == OK
#    # get a service id.
#    notification_id = response.json[0].get('id')
#    # get that service
#    response = client.get(f'{BASE_API}/notification/{notification_id}')
#    assert response.status_code == OK
#    response_content = response.json
#    del response_content['id']
#    assert response_content == user_notifications.get('1')
#
#
## CREATE QUEUES
# def test_post_queue_to_non_exist_404_error(client):
#    unexisting_notification = 'null'
#    response = client.get(f'{BASE_API}/notification/{unexisting_notification}/queues')
#    assert response.status_code == NOT_FOUND
#    assert response.json == NOT_FOUND_BODY
#
#
# def test_post_queue_exist_validation_error(client):
#    bad_queue = {
#        "name": "offering",
#        "endpoint": None
#    }
#    response = client.post(f'{BASE_API}/notification/{notification_id}/queues', json=bad_queue)
#    assert response.status_code == BODY_ERROR
#    assert response.json == QUEUE_ERROR
#
#
# def test_get_notification_queues_empty_list(client):
#    response = client.get(f'{BASE_API}/notification/{notification_id}/queues')
#    assert response.status_code == OK
#    assert response.json == []
#
#
# def test_post_queue(client):
#    global queue_id
#    response = client.post(f'{BASE_API}/notification/{notification_id}/queues', json=service_notifications)
#    assert response.status_code == OK
#    response_body = response.json
#    queue_id = response_body['id']
#    del response_body['id']
#    assert response_body == service_notifications
#
#
## GET QUEUE
# def test_get_queue_not_exist(client):
#    _uuid = uuid.uuid4().__str__()
#    print(f'service id: {notification_id}')
#    print(f'uuid: {_uuid}')
#    path = f'{BASE_API}/notification/{notification_id}/queues/{_uuid}'
#    print(path)
#    response = client.get(path)
#    assert response.status_code == NOT_FOUND
#    assert response.json == NOT_FOUND_BODY
#
#
# def test_get_queue_exist(client):
#    response = client.get(f'{BASE_API}/notification/{notification_id}/queues/{queue_id}')
#    assert response.status_code == OK
#    response_body = response.json
#    del response_body['id']
#    assert response_body == service_notifications
#
#
## GET ALL QUEUES
# def test_get_notification_queues(client):
#    response = client.get(f'{BASE_API}/notification/{notification_id}/queues')
#    assert response.status_code == OK
#    response_body = response.json
#    del response_body[0]['id']
#    assert response_body == [service_notifications]
#
#
## MODIFY QUEUE
# def test_deactivate_queue_dont_exist(client):
#    response = client.patch(f'{BASE_API}/notification/{notification_id}/queues/{uuid.uuid4().__str__()}/deactivate')
#    assert response.status_code == NOT_FOUND
#    assert response.json == NOT_FOUND_BODY
#
#
# def test_activate_queue_dont_exist(client):
#    response = client.patch(f'{BASE_API}/notification/{notification_id}/queues/{uuid.uuid4().__str__()}/activate')
#    assert response.status_code == NOT_FOUND
#    assert response.json == NOT_FOUND_BODY
#
#
# def test_deactivate_queue(client):
#    response = client.patch(f'{BASE_API}/notification/{notification_id}/queues/{queue_id}/deactivate')
#    assert response.status_code == OK
#    response_body = response.json
#    del response_body['id']
#    inverted_bool = service_notifications.copy()
#    inverted_bool['active'] = not inverted_bool['active']
#    assert inverted_bool == response_body
#
#
# def test_activate_queue(client):
#    response = client.patch(f'{BASE_API}/notification/{notification_id}/queues/{queue_id}/activate')
#    assert response.status_code == OK
#    response_body = response.json
#    del response_body['id']
#    assert response_body == response_body
#
#
## DELETE QUEUES
# def test_delete_queue_dont_exist(client):
#    response = client.delete(f'{BASE_API}/notification/{notification_id}/queues/{uuid.uuid4().__str__()}')
#    assert response.status_code == NOT_FOUND
#    assert response.json == NOT_FOUND_BODY
#
#
# def test_delete_queue_exist(client):
#    response = client.delete(f'{BASE_API}/notification/{notification_id}/queues/{queue_id}')
#    assert response.status_code == OK
#    response_body = response.json
#    del response_body['id']
#    assert response_body == service_notifications
#
#
# def test_delete_notification_dont_exist(client):
#    response = client.delete(f'{BASE_API}/notification/{uuid.uuid4().__str__()}')
#    assert response.status_code == NOT_FOUND
#    assert response.json == NOT_FOUND_BODY
#
#
# def test_delete_notification_exist(client):
#    response = client.delete(f'{BASE_API}/notification/{notification_id}')
#    assert response.status_code == OK
#    response_body = response.json
#    del response_body['id']
#    assert response_body == user_notifications.get('1')
#
