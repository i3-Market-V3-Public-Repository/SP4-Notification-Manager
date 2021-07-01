from flask import Blueprint, request, jsonify
from loguru import logger

from src.notification_manager.controller.service_queue_controller import QueueController
from src.notification_manager.models.queue import queue_to_object

api = Blueprint('queues', __name__)
# noinspection PyTypeChecker
__controller: QueueController = None


def config(controller: QueueController):
    global __controller
    __controller = controller


@api.route('/services', methods=['POST'])
def create_service():
    # {'nombre': ''}
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400
    result = __controller.create_service(request.json)

    if result is False:
        return jsonify({'error': 'Incomplete body'}), 400

    if result is None:
        return jsonify({'error': 'Already exists'}), 400

    return jsonify(result.to_json()), 200


@api.route('/services', methods=['GET'])
def get_services():
    # Traerlos todos
    pass


@api.route('/services/{services_id}/queues', methods=['POST'])
def post_queues(services_id: str):
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    queue = __controller.create_queue(request.json)
    # queues are stored by notifications_controller (services_queue_storage)
    return queue_to_object()


@api.route('/services/{services_id}/queues', defaults={"queue_id": None}, methods=['GET'])
@api.route('/services/{services_id}/queues/<queue_id>', methods=['GET'])
def get_queues(services_id: str, queue_id: str):
    pass


@api.route('/services/{services_id}/queues/<queue_id>', methods=['DELETE'])
def delete_queue(services_id: str, queue_id: str):
    pass


@api.route('/services/{services_id}/queues/<queue_id>', methods=['PUT'])
def put_queue(services_id: str, queue_id: str):
    pass


