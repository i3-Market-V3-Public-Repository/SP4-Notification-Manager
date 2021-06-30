from flask import Blueprint, request, jsonify
from loguru import logger

from src.storage.storage import Storage

api = Blueprint('queues', __name__)
# noinspection PyTypeChecker
__adapter: Storage = None


def config_database(adapter: Storage):
    global __adapter
    __adapter = adapter


# Expenses
@api.route('/services/{services_id}/queues', methods=['POST'])
def post_queues(services_id: str):
    pass


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
