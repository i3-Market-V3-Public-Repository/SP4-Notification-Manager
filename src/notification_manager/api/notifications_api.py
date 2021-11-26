from apiflask import APIBlueprint, output, input, abort
from flask import Blueprint, request, jsonify
from loguru import logger

from src.alert_subscription.controller.subscriptions_controller import SubscriptionsController
from src.notification_manager.controller.notifications_controller import NotificationsController
from src.notification_manager.controller.service_queue_controller import QueueController
from src.notification_manager.models.NotificationSwaggerModelsScheme import ServiceNotification, UserNotification, \
    Notification
from src.notification_manager.models.queue_types import QueueType

blueprint = APIBlueprint('notifications', __name__, url_prefix='/api/v1/')
# noinspection PyTypeChecker
__notification_controller: NotificationsController = None
# noinspection PyTypeChecker
__queue_controller: QueueController = None
# noinspection PyTypeChecker
__subscription_controller: SubscriptionsController = None


def config(notification_controller: NotificationsController,
           queue_controller: QueueController,
           subscription_controller: SubscriptionsController):
    global __notification_controller, __queue_controller, __subscription_controller
    __notification_controller = notification_controller
    __queue_controller = queue_controller
    __subscription_controller = subscription_controller


# ----------------------------SERVICE NOTIFICATIONS----------------------------------------
@blueprint.route('/notification/service', methods=['POST'])
@input(ServiceNotification)
def notification_service(self):
    data = request.json
    # {"receiver_id": "offering.new", "message": {"whatever"}"}
    if not data:
        # return jsonify({'error': 'Empty body'}), 400
        abort(400, "Empty body")

    if not data.get("receiver_id") or not isinstance(data.get("message"), dict):
        # return jsonify({"error": "Body has to contain receiver_id and message"}), 400
        abort(400, "Body has to container receiver_id and message {} with content")

    # extract receiver_id to get to which queue send the notification
    queue_name = data.get('receiver_id')
    message = data.get('message')
    logger.info("Received a notification to service: \n"
                "queue_name: {}, message: {}".format(queue_name, message))

    queues_endpoints = __queue_controller.search_services_by_queue_if_active(queue_name)
    # create the notification and send to them
    __notification_controller.send_notification_service(queue_name, queues_endpoints, message)

    # TODO: Modify downwards when services are separated, replace with requests.

    if queue_name == QueueType.NEWOFFERING.value:
        category = message.get('category')
        if category:
            # get users subscribed to that category
            users = __subscription_controller.search_users_by_category(category)  # { users: ["user1","user2"] }
            users = users.get('users')  # ["user1","user2"]
            for user in users:
                # create a user notification to that category
                __notification_controller.send_notification_user(user, 'i3-market', 'Ok', QueueType.NEWOFFERING.value,
                                                                 True, message)
        else:
            logger.warning('Notification about new offering but no category in message!')
    return jsonify(), 200


# ----------------------------USER NOTIFICATIONS----------------------------------------
# @blueprint.route('/notification/user', methods=['POST'])
@input(UserNotification)
@output(Notification)
@blueprint.route('/notification', methods=['POST'])
def notification_user():
    if not request.json:
        # return jsonify({'error': 'Empty body'}), 400
        abort(400, 'Empty body')

    if not request.json.get('receiver_id') or not request.json.get("message"):
        # return jsonify({"error": "Body has to contain receiver_id and message"}), 400
        abort(400, 'Body has to contain data')

    data = request.json
    destiny_user_id = data.get("receiver_id")
    origin = data.get("origin")
    status = data.get('status')
    _type = data.get('type')
    # _sub_type = data.get('sub_type')
    predefined = data.get("predefined")
    message = data.get('message')
    logger.info("Received a request to notify user {}".format(destiny_user_id))
    stored_notification = __notification_controller.send_notification_user(destiny_user_id, origin, status, _type,
                                                                           predefined, message)
    # logger.info("Stored Notification: {}".format(stored_notification))

    return jsonify(stored_notification), 200


# @blueprint.route('/notification/', methods=['GET'])
@output(Notification(many=True))
@blueprint.route('/notification', methods=['GET'])
def get_notifications():
    return jsonify(__notification_controller.get_all_notifications()), 200


@output(Notification(many=True))
@blueprint.route('/notification/user/<user_id>', methods=['GET'])
def get_notification_by_userid(user_id: str):
    result = __notification_controller.get_user_notification(user_id)
    if result:
        return jsonify(__notification_controller.get_user_notification(user_id)), 200
    else:
        return jsonify(), 404


# @blueprint.route('/notification/unread/', methods=['GET'])
@output(Notification(many=True))
@blueprint.route('/notification/unread', methods=['GET'])
def get_unread_notifications():
    return jsonify(__notification_controller.get_all_unread_notifications()), 200


# @blueprint.route('/notification/user/<user_id>/unread/', methods=['GET'])
@output(Notification(many=True))
@blueprint.route('/notification/user/<user_id>/unread', methods=['GET'])
def get_unread_notifications_by_id(user_id: str):
    return jsonify(__notification_controller.get_unread_user_notification(user_id)), 200


# @blueprint.route('/notification/<notification_id>/', methods=['GET'])
@output(Notification)
@blueprint.route('/notification/<notification_id>', methods=['GET'])
def get_notification(notification_id: str):
    result = __notification_controller.get_notification(notification_id)
    if result:
        return jsonify(result), 200
    return jsonify(), 404


@output(Notification)
@blueprint.route('/notification/<notification_id>/read', methods=['PATCH'])
@blueprint.route('/notification/<notification_id>/unread', methods=['PATCH'])
def modify_notification(notification_id: str):
    read = request.path.split('/')[-1] == 'read'
    result = __notification_controller.modify_notification(notification_id, read)
    if result:
        return jsonify(result), 200
    # return jsonify(), 404
    abort(404, "Notification not found")


@output(Notification)
@blueprint.route('/notification/<notification_id>', methods=['DELETE'])
def delete_notification(notification_id: str):
    result = __notification_controller.delete_notification(notification_id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify(), 404
