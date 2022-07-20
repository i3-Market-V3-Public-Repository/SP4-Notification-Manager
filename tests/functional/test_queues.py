import uuid
from _pytest.recwarn import warns
from loguru import logger
from tests import BASE_API, OK_CODE, BODY_ERROR_CODE, NOT_FOUND_CODE, ALREADY_EXIST_SERVICE_BODY, NOT_FOUND_BODY, QUEUE_ERROR_BODY

services = {
    '1':
        {
            "endpoint": "string",
            "name": "service-test",
            "marketId": None,
            # 'queues': []
        }
}
services_output = services.get('1').copy()
services_output['queues'] = []
queue = {
    "name": "offering.new",
    "endpoint": None,
    #"active": True
}
queue_output = queue.copy()
queue_output['active'] = True

service_id = ''
queue_id = ''


# RETURN ALL REGISTERED SERVICES
def test_retrieve_all_services_return_empty_list(client):
    response = client.get(f'{BASE_API}/services')
    assert response.status_code == OK_CODE
    assert response.json == []


# CREATE SERVICE
def test_create_service_with_empty_body_return_400_error_no_body(client):
    response = client.post(f'{BASE_API}/services')
    assert response.status_code == BODY_ERROR_CODE
    assert response.json == {'detail': {'json': {'name': ['Missing data for required field.']}},
                             'message': 'Validation error'}


def test_create_service_with_empty_body_return_400_error_incomplete(client):
    response = client.post(f'{BASE_API}/services', json={"a": "b"})

    assert response.status_code == BODY_ERROR_CODE
    assert response.json == {'detail': {'json': {'a': ['Unknown field.'],
                                                 'name': ['Missing data for required field.']}},
                             'message': 'Validation error'}


def test_create_service_with_body_return_created(client):
    global service_id
    response = client.post(f'{BASE_API}/services', json=services.get('1'))

    response_body = response.json
    service_id = response_body.get('id')
    if service_id:
        del response_body['id']
    else:
        raise Exception(f'No service ID found, {response_body}')

    assert response.status_code == OK_CODE
    # assert response_body == services.get('1')
    assert response_body == services_output


def test_create_service_with_body_return_created_400_already_exist(client):
    response = client.post(f'{BASE_API}/services', json=services.get('1'))
    assert response.status_code == BODY_ERROR_CODE
    assert response.json == ALREADY_EXIST_SERVICE_BODY


# RETRIEVE EXISTING SERVICES
def test_retrieve_all_services_return_service_lists(client):
    global service_id, service_id
    response = client.get(f'{BASE_API}/services')

    response_body = response.json
    for service in response_body:
        logger.info(f'service id: {service_id}')
        service_id = service['id']
        del service['id']

    assert response.status_code == OK_CODE
    assert response_body == [services_output]


def test_retrieve_missing_service_return_404_error_not_found(client):
    response = client.get(f'{BASE_API}/services/{uuid.uuid4().__str__()}')
    assert response.status_code == 404
    assert response.json == NOT_FOUND_BODY


def test_retrieve_service_by_id_return_object(client):
    global service_id
    # get that service
    response = client.get(f'{BASE_API}/services/{service_id}')
    assert response.status_code == OK_CODE
    response_content = response.json
    del response_content['id']
    assert response_content == services_output


# CREATE QUEUES
def test_post_queue_to_non_exist_404_error(client):
    unexisting_service = 'null0'
    response = client.get(f'{BASE_API}/services/{unexisting_service}/queues')
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_post_queue_exist_validation_error(client):
    bad_queue = {
        "name": "offering",
        "endpoint": None
    }
    response = client.post(f'{BASE_API}/services/{service_id}/queues', json=bad_queue)
    assert response.status_code == BODY_ERROR_CODE
    assert response.json == QUEUE_ERROR_BODY


def test_get_service_queues_empty_list(client):
    response = client.get(f'{BASE_API}/services/{service_id}/queues')
    assert response.status_code == OK_CODE
    assert response.json == []


def test_post_queue_200_success(client):
    global queue_id
    response = client.post(f'{BASE_API}/services/{service_id}/queues', json=queue)
    logger.warning(f'response: {response.json}')
    assert response.status_code == OK_CODE
    response_body = response.json
    queue_id = response_body.get('id')
    del response_body['id']
    assert response_body == queue_output


# GET QUEUE
def test_get_queue_not_exist(client):
    _uuid = uuid.uuid4().__str__()
    logger.info(f'service id: {service_id}')
    logger.info(f'uuid: {_uuid}')
    path = f'{BASE_API}/services/{service_id}/queues/{_uuid}'
    logger.info(path)
    response = client.get(path)
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_get_queue_exist(client):
    response = client.get(f'{BASE_API}/services/{service_id}/queues/{queue_id}')
    assert response.status_code == OK_CODE
    response_body = response.json
    del response_body['id']
    assert response_body == queue_output


# GET ALL QUEUES
def test_get_service_queues(client):
    response = client.get(f'{BASE_API}/services/{service_id}/queues')
    assert response.status_code == OK_CODE
    response_body = response.json
    del response_body[0]['id']
    assert response_body == [queue_output]


# MODIFY QUEUE
def test_deactivate_queue_dont_exist(client):
    response = client.patch(f'{BASE_API}/services/{service_id}/queues/{uuid.uuid4().__str__()}/deactivate')
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_activate_queue_dont_exist(client):
    response = client.patch(f'{BASE_API}/services/{service_id}/queues/{uuid.uuid4().__str__()}/activate')
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_deactivate_queue(client):
    response = client.patch(f'{BASE_API}/services/{service_id}/queues/{queue_id}/deactivate')
    assert response.status_code == OK_CODE
    response_body = response.json
    del response_body['id']
    inverted_bool = queue_output.copy()
    inverted_bool['active'] = not inverted_bool['active']
    assert inverted_bool == response_body


def test_activate_queue(client):
    response = client.patch(f'{BASE_API}/services/{service_id}/queues/{queue_id}/activate')
    assert response.status_code == OK_CODE
    response_body = response.json
    del response_body['id']
    assert response_body == response_body


# DELETE QUEUES
def test_delete_queue_dont_exist(client):
    response = client.delete(f'{BASE_API}/services/{service_id}/queues/{uuid.uuid4().__str__()}')
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_delete_queue_exist(client):
    response = client.delete(f'{BASE_API}/services/{service_id}/queues/{queue_id}')
    assert response.status_code == OK_CODE
    response_body = response.json
    del response_body['id']
    assert response_body == queue_output


def test_delete_service_dont_exist(client):
    response = client.delete(f'{BASE_API}/services/{uuid.uuid4().__str__()}')
    assert response.status_code == NOT_FOUND_CODE
    assert response.json == NOT_FOUND_BODY


def test_delete_service_exist(client):
    response = client.delete(f'{BASE_API}/services/{service_id}')
    assert response.status_code == OK_CODE
    response_body = response.json
    del response_body['id']
    assert response_body == services_output
