from flask import Blueprint, request, jsonify
from loguru import logger
from apiflask import APIBlueprint, abort
from src.notification_manager.controller.service_queue_controller import QueueController
from src.notification_manager.models.NotificationSwaggerModelsScheme import Service, ServiceInput, \
    QueueInput, Queue

blueprint = APIBlueprint('queues', __name__, url_prefix='/api/v1/')
# noinspection PyTypeChecker
__controller: QueueController = None


def config(controller: QueueController):
    global __controller
    __controller = controller


@blueprint.route('/services/<service_id>', methods=['GET'])
@blueprint.output(Service)
def get_services_by_id(service_id: str):
    result = __controller.retrieve_service(service_id)
    if result:
        return result.to_json()
    abort(404, 'Not Found')


@blueprint.route('/services', methods=['GET'])
@blueprint.output(Service(many=True), example=[
    {
        "id": "84744b8b-fb2d-4a16-9d86-6b1a2cd34c62",
        "name": "i3-market-test",
        "marketId": None,
        "endpoint": "https://webhook.site/11798498-a25a-429c-ac11-8d2d9aa26e83",
        "queues": [
            {
                "id": "b11807ce-17ad-416f-9bd1-bdf9dd049dcf",
                "name": "offering.new",
                "endpoint": None,
                "active": False
            }
        ]
    }
])
def get_services():
    result = __controller.retrieve_all()
    return result


########################################################################################################################
# SERVICES API
########################################################################################################################


# @blueprint.route('/services', methods=['POST'])
@blueprint.post('/services')
@blueprint.output(Service, example={
    "id": "123445-123-1245-12345-12354566773",
    "marketId": None,
    "name": "service-test-2",
    "endpoint": "https://test-server:1234/endpoint",
    "queues": []
})
@blueprint.input(ServiceInput)
def create_service(data):
    result = __controller.create_service(data)

    if result is False:
        abort(400, 'Incomplete Body')

    if result is None:
        abort(400, 'Already exists')

    return result.to_json()


@blueprint.route('/services/<service_id>', methods=['DELETE'])
@blueprint.output(Service)
def delete_service(service_id: str):
    result = __controller.delete_service(service_id)

    if result is None:
        abort(404, 'Not Found')

    return result.to_json()


########################################################################################################################
# QUEUES API
########################################################################################################################
@blueprint.route('/services/<service_id>/queues', methods=['GET'])
@blueprint.output(Queue(many=True), example=[
    {
        "id": "b11807ce-17ad-416f-9bd1-bdf9dd049dcf",
        "name": "offering.new",
        "endpoint": None,
        "active": False
    }
])
def get_queues(service_id: str):
    result = __controller.retrieve_service_queues(service_id)
    if result is None:
        abort(404, 'Not Found')
    else:
        return [s.to_json() for s in result]


@blueprint.route('/services/<service_id>/queues/<queue_id>', methods=['GET'])
@blueprint.output(Queue)
def get_queues_by_id(service_id: str, queue_id: str):
    result = __controller.retrieve_service_queues(service_id, queue_id)

    if result is None:
        abort(404, 'Not Found')

    if not queue_id:
        return [s.to_json() for s in result]

    return result.to_json()


@blueprint.route('/services/<service_id>/queues', methods=['POST'])
@blueprint.input(QueueInput())
@blueprint.output(Queue, example={
    "id": "asd124-ergh1-5673-456345-sdf879efw78",
    "name": "offering.update",
    "endpoint": "https://webhook.site/11798498-a25a-429c-ac11-8d2d9aa26e83",
    "active": True
})
def post_queues(service_id: str, data: dict):
    result = __controller.create_queue(service_id, data)
    # queues are stored by notifications_controller (services_queue_storage)
    if result is False:
        abort(400, 'Incomplete Body')
    if result is None:
        abort(400, 'Already exists service queue')
    if result == -1:
        abort(400, 'Queue Type doesn`t exist')
    return result.to_json()


@blueprint.route('/services/<service_id>/queues/<queue_id>', methods=['DELETE'])
@blueprint.output(Queue)
def delete_queue(service_id: str, queue_id: str):
    result = __controller.delete_queue(service_id, queue_id)

    if result is None:
        abort(404, 'Not Found')

    return result.to_json()


# TODO Implement the update of a service and queue
# @api.route('/services/<service_id>/queues/<queue_id>', methods=['PUT'])
# def put_queue(service_id: str, queue_id: str):
#     result = __controller.update_queue(service_id, queue_id, request.json())
#     if result is None:
#         abort(404, 'Not Found')
#
#     return jsonify(result.to_json()), 200


@blueprint.route('/services/<service_id>/queues/<queue_id>/activate', methods=['PATCH'])
@blueprint.route('/services/<service_id>/queues/<queue_id>/deactivate', methods=['PATCH'])
@blueprint.output(Queue)
def switch_status_queue(service_id: str, queue_id: str):
    activated = request.path.split('/')[-1] == 'activate'

    result = __controller.switch_status_queue(service_id, queue_id, activated)

    if result is None:
        abort(404, 'Not Found')

    return result.to_json()
