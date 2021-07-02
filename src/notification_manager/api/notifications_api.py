from flask import Blueprint, request, jsonify
from loguru import logger
from src.notification_manager.controller.notifications_controller import NotificationsController
from src.notification_manager.controller.service_queue_controller import QueueController

api = Blueprint('notifications', __name__)
# noinspection PyTypeChecker
__notification_controller: NotificationsController = None
__queue_controller: QueueController = None


def config(notification_controller: NotificationsController, queue_controller: QueueController):
    global __notification_controller, __queue_controller
    __notification_controller = notification_controller
    __queue_controller = queue_controller


@api.route('/notification/service', methods=['POST'])
def notification_service():
    # {"receiver_id": "offering.new", "message": loquesea}
    if not request.json:

        return jsonify({'error': 'Empty body'}), 400

    # TODO añadir comprobacion campos
    # extract receiver_id to get to which queue send the notification
    queue_name = request.json.get('receiver_id')
    queues_endpoints = __queue_controller.search_services_by_queue(queue_name)
    # create the notification and send to them
    __notification_controller.send_notification_service(queue_name, queues_endpoints, request.json)


@api.route('/notification/user', methods=['POST'])
def notification_user():
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400
    # TODO implement THIS! release v2
    return jsonify({'error': 'Method not implemented yet'}), 501
