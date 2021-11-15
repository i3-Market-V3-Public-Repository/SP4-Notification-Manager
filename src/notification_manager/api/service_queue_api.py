from apiflask import APIBlueprint
from flask import Blueprint, request, jsonify
from loguru import logger

from src.notification_manager.controller.service_queue_controller import QueueController
from src.notification_manager.models.queue import queue_to_object

blueprint = APIBlueprint('queues', __name__, url_prefix='/api/v1/')
# noinspection PyTypeChecker
__controller: QueueController = None


def config(controller: QueueController):
    global __controller
    __controller = controller


@blueprint.route('/services', methods=['GET'])
def get_services():
    result = __controller.retrieve_all()
    return jsonify(result), 200


########################################################################################################################
# SERVICES API
########################################################################################################################
@blueprint.route('/services', methods=['POST'])
def create_service():
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    result = __controller.create_service(request.json)

    if result is False:
        return jsonify({'error': 'Incomplete body'}), 400

    if result is None:
        return jsonify({'error': 'Already exists'}), 400

    return jsonify(result.to_json()), 200


@blueprint.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id: str):
    result = __controller.delete_service(service_id)

    if result is None:
        return jsonify({'error': 'Not found'}), 400

    return jsonify(result.to_json()), 200


########################################################################################################################
# QUEUES API
########################################################################################################################
@blueprint.route('/services/<service_id>/queues', defaults={"queue_id": None}, methods=['GET'])
@blueprint.route('/services/<service_id>/queues/<queue_id>', methods=['GET'])
def get_queues(service_id: str, queue_id: str):
    result = __controller.retrieve_service_queues(service_id, queue_id)

    if result is None:
        return jsonify({'error': 'Not found'}), 404

    if not queue_id:
        return jsonify([s.to_json() for s in result]), 200

    return jsonify(result.to_json()), 200


@blueprint.route('/services/<service_id>/queues', methods=['POST'])
def post_queues(service_id: str):
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    result = __controller.create_queue(service_id, request.json)
    # queues are stored by notifications_controller (services_queue_storage)
    if result is False:
        return jsonify({'error': 'Incomplete body'}), 400
    if result is None:
        return jsonify({'error': 'Already exists service queue'}), 400
    if result == -1:
        return jsonify({'error': 'Queue Type doesn`t exist'}), 400
    return jsonify(result.to_json()), 200


@blueprint.route('/services/<service_id>/queues/<queue_id>', methods=['DELETE'])
def delete_queue(service_id: str, queue_id: str):
    result = __controller.delete_queue(service_id, queue_id)

    if result is None:
        return jsonify({'error': 'Not found'}), 400

    return jsonify(result.to_json()), 200


# @api.route('/services/<service_id>/queues/<queue_id>', methods=['PUT'])
# def put_queue(service_id: str, queue_id: str):
#     result = __controller.update_queue(service_id, queue_id, request.json())
#     if result is None:
#         return jsonify({'error': 'Not found'}), 400
#
#     return jsonify(result.to_json()), 200


@blueprint.route('/services/<service_id>/queues/<queue_id>/activate', methods=['POST'])
@blueprint.route('/services/<service_id>/queues/<queue_id>/deactivate', methods=['POST'])
def status_queue(service_id: str, queue_id: str):
    activated = request.path.split('/')[-1] == 'activate'

    result = __controller.switch_status_queue(service_id, queue_id, activated)

    if result is None:
        return jsonify({'error': 'Not found'}), 400

    return jsonify(result.to_json()), 200
