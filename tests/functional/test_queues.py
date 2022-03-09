import uuid
from _pytest.recwarn import warns

from tests import BASE_API, OK, BODY_ERROR, NOT_FOUND, EMPTY_BODY, INCOMPLETE_BODY, ALREADY_EXIST_BODY_SERVICE, \
    NOT_FOUND_BODY, QUEUE_ERROR

services = {
    '1':
        {
            "endpoint": "string",
            "name": "service-test",
            "marketId": None,
            'queues': []
        }
}

queue = {
        "name": "offering.new",
        "endpoint": None,
        "active": True
}

notification_id = ''
queue_id = ''


# RETURN ALL REGISTERED SERVICES
def test_retrieve_all_services_return_empty_list(client):
    response = client.get(f'{BASE_API}/services')
    assert response.status_code == OK
    assert response.json == []


# CREATE SERVICE
def test_create_service_with_empty_body_return_400_error_no_body(client):
    response = client.post(f'{BASE_API}/services')
    assert response.status_code == BODY_ERROR
    assert response.json == EMPTY_BODY


def test_create_service_with_empty_body_return_400_error_incomplete(client):
    response = client.post(f'{BASE_API}/services', json={"a":"b"})

    assert response.status_code == BODY_ERROR
    assert response.json == INCOMPLETE_BODY


def test_create_service_with_body_return_created(client):
    response = client.post(f'{BASE_API}/services', json=services.get('1'))

    response_body = response.json
    del response_body['id']

    assert response.status_code == OK
    assert response_body == services.get('1')


def test_create_service_with_body_return_created_400_already_exist(client):
    response = client.post(f'{BASE_API}/services', json=services.get('1'))
    assert response.status_code == BODY_ERROR
    assert response.json == ALREADY_EXIST_BODY_SERVICE


# RETRIEVE EXISTING SERVICES
def test_retrieve_all_services_return_service_lists(client):
    global notification_id
    response = client.get(f'{BASE_API}/services')

    response_body = response.json
    for service in response_body:
        service_id = service['id']
        del service['id']

    assert response.status_code == OK
    assert response_body == [services.get('1')]


def test_retrieve_missing_service_return_404_error_not_found(client):
    response = client.get(f'{BASE_API}/services/{uuid.uuid4().__str__()}')
    assert response.status_code == 404
    assert response.json == NOT_FOUND_BODY


def test_retrieve_service_by_id_return_object(client):
    global notification_id
    # get all registered services
    path = f'{BASE_API}/services'
    response = client.get(path)
    assert response.status_code == OK
    # get a service id.
    service_id = response.json[0].get('id')
    # get that service
    response = client.get(f'{BASE_API}/services/{service_id}')
    assert response.status_code == OK
    response_content = response.json
    del response_content['id']
    assert response_content == services.get('1')


# CREATE QUEUES
def test_post_queue_to_non_exist_404_error(client):
    unexisting_service = 'null'
    response = client.get(f'{BASE_API}/services/{unexisting_service}/queues')
    assert response.status_code == NOT_FOUND
    assert response.json == NOT_FOUND_BODY


def test_post_queue_exist_validation_error(client):
    bad_queue = {
        "name": "offering",
        "endpoint": None
    }
    response = client.post(f'{BASE_API}/services/{notification_id}/queues', json=bad_queue)
    assert response.status_code == BODY_ERROR
    assert response.json == QUEUE_ERROR


def test_get_service_queues_empty_list(client):
    response = client.get(f'{BASE_API}/services/{notification_id}/queues')
    assert  response.status_code == OK
    assert response.json == []


def test_post_queue(client):
    global queue_id
    response = client.post(f'{BASE_API}/services/{notification_id}/queues', json=queue)
    assert response.status_code == OK
    response_body = response.json
    queue_id = response_body['id']
    del response_body['id']
    assert response_body == queue


# GET QUEUE
def test_get_queue_not_exist(client):
    _uuid = uuid.uuid4().__str__()
    print(f'service id: {notification_id}')
    print(f'uuid: {_uuid}')
    path = f'{BASE_API}/services/{notification_id}/queues/{_uuid}'
    print(path)
    response = client.get(path)
    assert response.status_code == NOT_FOUND
    assert response.json == NOT_FOUND_BODY


def test_get_queue_exist(client):
    response = client.get(f'{BASE_API}/services/{notification_id}/queues/{queue_id}')
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    assert response_body == queue


# GET ALL QUEUES
def test_get_service_queues(client):
    response = client.get(f'{BASE_API}/services/{notification_id}/queues')
    assert response.status_code == OK
    response_body = response.json
    del response_body[0]['id']
    assert response_body == [queue]


# MODIFY QUEUE
def test_deactivate_queue_dont_exist(client):
    response = client.patch(f'{BASE_API}/services/{notification_id}/queues/{uuid.uuid4().__str__()}/deactivate')
    assert response.status_code == NOT_FOUND
    assert response.json == NOT_FOUND_BODY


def test_activate_queue_dont_exist(client):
    response = client.patch(f'{BASE_API}/services/{notification_id}/queues/{uuid.uuid4().__str__()}/activate')
    assert response.status_code == NOT_FOUND
    assert response.json == NOT_FOUND_BODY


def test_deactivate_queue(client):
    response = client.patch(f'{BASE_API}/services/{notification_id}/queues/{queue_id}/deactivate')
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    inverted_bool = queue.copy()
    inverted_bool['active'] = not inverted_bool['active']
    assert inverted_bool == response_body


def test_activate_queue(client):
    response = client.patch(f'{BASE_API}/services/{notification_id}/queues/{queue_id}/activate')
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    assert response_body == response_body


# DELETE QUEUES
def test_delete_queue_dont_exist(client):
    response = client.delete(f'{BASE_API}/services/{notification_id}/queues/{uuid.uuid4().__str__()}')
    assert response.status_code == NOT_FOUND
    assert response.json == NOT_FOUND_BODY


def test_delete_queue_exist(client):
    response = client.delete(f'{BASE_API}/services/{notification_id}/queues/{queue_id}')
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    assert response_body == queue


def test_delete_service_dont_exist(client):
    response = client.delete(f'{BASE_API}/services/{uuid.uuid4().__str__()}')
    assert response.status_code == NOT_FOUND
    assert response.json == NOT_FOUND_BODY


def test_delete_service_exist(client):
    response = client.delete(f'{BASE_API}/services/{notification_id}')
    assert response.status_code == OK
    response_body = response.json
    del response_body['id']
    assert response_body == services.get('1')



