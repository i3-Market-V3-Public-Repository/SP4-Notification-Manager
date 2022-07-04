import uuid
from datetime import datetime
from _pytest.recwarn import warns

from tests import BASE_API, OK, BODY_ERROR, NOT_FOUND, EMPTY_BODY, INCOMPLETE_BODY, ALREADY_EXIST_BODY_SERVICE, \
    NOT_FOUND_BODY, QUEUE_ERROR, ALREADY_EXIST_BODY

output_notification = {'action': 'offering.new',
                       'data': {'category': 'Agriculture', 'msg': 'this is a new offering'},
                       'origin': 'string',
                       'receptor': 'UserID123',
                       'status': 'string',
                       'unread': True,
                       'dateCreated': datetime.utcnow().strftime("%Y/%m/%dT%H:%M:%SZ")}
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

market_id = 'market1'

service_notifications = {
    '1':
        {
            "receiver_id": "offering.new",
            "message": {"msg": "this is a message!"}
        },
    '2':
        {
            "receiver_id": "agreement.claim",
            "message": {"marketId": market_id, "msg": "this is a message!"}
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


def test_create_user_notification_with_body_return_created(client):
    global notification_id
    response = client.post(f'{BASE_API}/notification', json=user_notifications.get('1'))

    response_body = response.json
    notification_id = response_body.get('id')
    del response_body['id']

    assert response.status_code == OK
    assert response_body == output_notification


# RETRIEVE EXISTING USER NOTIFICATIONS
def test_retrieve_all_notifications_return_notification_lists(client):
    global notification_id
    response = client.get(f'{BASE_API}/notification/user/{user_notifications.get("1").get("receiver_id")}')
    response_body = response.json
    del response_body[0]['id']
    assert response.status_code == OK
    assert response_body == [output_notification]


def test_retrieve_missing_notification_return_404_error_not_found(client):
    response = client.get(f'{BASE_API}/notification/user/random')
    assert response.status_code == 404
    assert response.json == NOT_FOUND_BODY


def test_retrieve_notification_by_id_return_object(client):
    global notification_id
    # get all registered services
    path = f'{BASE_API}/notification'
    response = client.get(path)
    assert response.status_code == OK
    # get a service id.
    notification_id = response.json[0].get('id')
    # get that service
    response = client.get(f'{BASE_API}/notification/{notification_id}')
    assert response.status_code == OK
    response_content = response.json
    del response_content['id']
    assert response_content == output_notification


#  MODIFY USER NOTIFICATIONS
def test_modify_read_notification_not_exist_return_404(client):
    path = f'{BASE_API}/notification/asd/read'
    response = client.patch(path)
    assert response.status_code == NOT_FOUND
    NOT_FOUND_NOT = NOT_FOUND_BODY
    NOT_FOUND_NOT['message'] = 'Notification not found'
    assert response.json == NOT_FOUND_NOT


def test_modify_unread_notification_not_exist_return_404(client):
    path = f'{BASE_API}/notification/asd/unread'
    response = client.patch(path)
    assert response.status_code == NOT_FOUND
    NOT_FOUND_NOT = NOT_FOUND_BODY
    NOT_FOUND_NOT['message'] = 'Notification not found'
    assert response.json == NOT_FOUND_NOT


def test_modify_read_notification_return_sucess(client):
    path = f'{BASE_API}/notification/{notification_id}/read'
    response = client.patch(path)
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    assert response_body == {'action': 'offering.new',
                             'data': {'category': 'Agriculture', 'msg': 'this is a new offering'},
                             'origin': 'string',
                             'receptor': 'UserID123',
                             'status': 'string',
                             'unread': False,
                             'dateCreated': output_notification['dateCreated']}


def test_modify_unread_notification_return_sucess(client):
    path = f'{BASE_API}/notification/{notification_id}/unread'
    response = client.patch(path)
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    assert response_body == {'action': 'offering.new',
                             'data': {'category': 'Agriculture', 'msg': 'this is a new offering'},
                             'origin': 'string',
                             'receptor': 'UserID123',
                             'status': 'string',
                             'unread': True,
                             'dateCreated': output_notification['dateCreated']}


# MARKETPLACE NOTIFICATIONS
services = {
    '1':
        {
            # "endpoint": "http://localhost:2000",
            "endpoint": "https://eozfc9xreuvfipx.m.pipedream.net",
            "name": "service-test",
            "marketId": market_id,
            'queues': []
        }
}

queue = {
    "name": "agreement.claim",
    "endpoint": None,
    "active": True
}

service_id = ''
queue_id = ''


def test_marketplace_service_notification_200_success(client):
    # register service
    # to terminal ➜ nc -l -p 2000 -k
    global service_id
    response = client.post(f'{BASE_API}/services', json=services.get('1'))
    response_body = response.json
    service_id = response_body.get('id')
    if service_id:
        del response_body['id']

    # assert response.status_code == OK
    assert response_body == services.get('1')

    # register queue
    global queue_id
    response = client.post(f'{BASE_API}/services/{service_id}/queues', json=queue)
    assert response.status_code == OK
    response_body = response.json
    queue_id = response_body['id']
    if queue_id:
        del response_body['id']
    assert response_body == queue
    # create service notitication
    response = client.post(f'{BASE_API}/notification/service', json=service_notifications['2'])
    response_body = response.json
    assert response_body == [{'destiny': services.get('1').get('name'), 'response': 200}]

# TODO ADD MORE SERVICE NOTIFICATIONS
