from flask import Blueprint, request, jsonify
from loguru import logger
from src.notification_manager.controller.notifications_controller import NotificationsController

api = Blueprint('queues', __name__)
# noinspection PyTypeChecker
__controller: NotificationsController = None


def config(controller: NotificationsController):
    global __controller
    __controller = controller


@api.route('/notification/service', methods=['POST'])
def notification_service():
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400
    # TODO needed check if queue exist and if not is created/return error?
    pass


@api.route('/notification/user', methods=['POST'])
def notification_user():
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400
    # TODO implement THIS! release v2
    pass
