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
    logger.info("Received a notification to service: \n"
                "queue_name: {}, message: {}".format(queue_name, message))
    queues_endpoints = __queue_controller.search_services_by_queue_if_active(queue_name)
    # create the notification and send to them
    __notification_controller.send_notification_service(queue_name, queues_endpoints, message)

    # TODO: Eliminar hacia abajo linea cuando se separen los servicios, sustituir por requests.
    category = message.get('category')
    __subscription_controller.search_users_by_subscription(category, message=request.json)

    return jsonify(), 200


@api.route('/notification/user', methods=['POST'])
def notification_user():
    """
    {
        "receiver_id": "string",    # DESTINY USER ID TO SEND NOTIFICATION
        "type": "string",           # [OFFERING, CONTRACT MANAGER, etc]
        "sub_type": "string",       # [UPDATE, REJECT, etc]
        "predefined": true,         # always true?
        "message": "string"         # DATA OF THE MESSAGE
    }
    """
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    if not request.json.get('receiver_id') or not request.json.get("message"):
        return jsonify({"error": "Body has to contain receiver_id and message"}), 400

    data = request.json
    destiny_user_id = data.get("receiver_id")
    _type = data.get('type')
    _sub_type = data.get('sub_type')
    predefined = data.get("predefined")
    message = data.get('message')
    logger.info("Received a request to notify user {}".format(destiny_user_id))
    stored_notification = __notification_controller.send_notification_user(destiny_user_id,_type,_sub_type,predefined,message)
    logger.info("Stored Notification: {}".format(stored_notification))

    return jsonify(), 200


@api.route('/notification/user', methods=['GET'])
@api.route('/notification/user/', methods=['GET'])
@api.route('/notification/user/<user_id>', methods=['GET'])
def get_notifications(user_id=None):
    if user_id:
        return __notification_controller.get_user_notification(user_id)

    else:
        return __notification_controller.get_all_notifications()
