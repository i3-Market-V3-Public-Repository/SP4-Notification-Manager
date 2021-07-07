from flask import Blueprint, request, jsonify
from loguru import logger

from src.alert_subscription.controller.subscriptions_controller import SubscriptionsController
from src.notification_manager.controller.notifications_controller import NotificationsController
from src.notification_manager.controller.service_queue_controller import QueueController

api = Blueprint('notifications', __name__, url_prefix='/api/v1/')
# noinspection PyTypeChecker
__notification_controller: NotificationsController = None
__queue_controller: QueueController = None
__subscription_controller: SubscriptionsController = None


def config(notification_controller: NotificationsController,
           queue_controller: QueueController,
           subscription_controller: SubscriptionsController):
    global __notification_controller, __queue_controller, __subscription_controller
    __notification_controller = notification_controller
    __queue_controller = queue_controller
    __subscription_controller = subscription_controller


@api.route('/notification/service', methods=['POST'])
def notification_service():
    # {"receiver_id": "offering.new", "message": loquesea}
    if not request.json:

        return jsonify({'error': 'Empty body'}), 400

    if not request.json.get("receiver_id") or not request.json.get("message"):
        return jsonify({"error": "Body has to contain receiver_id and message"}), 400

    # extract receiver_id to get to which queue send the notification
    queue_name = request.json.get('receiver_id')
    message = request.json.get('message')

    queues_endpoints = __queue_controller.search_services_by_queue(queue_name)
    # create the notification and send to them
    __notification_controller.send_notification_service(queue_name, queues_endpoints, message)
    # TODO: Eliminar esta linea cuando se separen los servicios
    category = message.get('category')
    __subscription_controller.search_users_by_subscription(category, message=request.json)

    return jsonify(), 200


@api.route('/notification/user', methods=['POST'])
def notification_user():
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400
    # TODO implement THIS! release v2
    return jsonify({'error': 'Method not implemented yet'}), 501
