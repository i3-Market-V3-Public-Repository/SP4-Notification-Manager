from flask import Blueprint, request, jsonify
from loguru import logger

from src.notification_manager.controller.queue_controller import QueueController

api = Blueprint('queues', __name__)
# noinspection PyTypeChecker
__controller: QueueController = None


def config(controller: QueueController):
    global __controller
    __controller = controller


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



@api.route('/services', methods=['POST'])
# {'nombre': ''}

@api.route('/services', methods=['GET'])
# Traerlos todos

@api.route('/services/{services_id}/queues', methods=['POST'])


@api.route('/services/{services_id}/queues', defaults={"queue_id": None}, methods=['GET'])
@api.route('/services/{services_id}/queues/<queue_id>', methods=['GET'])

@api.route('/services/{services_id}/queues/<queue_id>', methods=['DELETE'])
@api.route('/services/{services_id}/queues/<queue_id>', methods=['PUT'])