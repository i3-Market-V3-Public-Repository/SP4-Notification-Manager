from apiflask import APIBlueprint, abort
from flask import request, jsonify
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
@blueprint.input(ServiceNotification)
def notification_service(data):
    # {"receiver_id": "offering.new", "message": {"whatever"}"}

    if not data.get("receiver_id") or not isinstance(data.get("message"), dict):
        abort(400, "Body has to container receiver_id and message {} with content")

    # data extraction
    queue_name = data.get('receiver_id')
    message = data.get('message')

    logger.info("Received a notification to service: \n"
                "queue_name: {}, message: {}".format(queue_name, message))

    # request to only one marketplace
    market_id = message.get('marketId') or message.get('MarketId')

    if market_id:
        # if exist a registered service with this market_id, create a notification and send only to this service
        service = __queue_controller.search_services_by_market_id_if_active(market_id, queue_name)
        response = __notification_controller.create_service_notification(queue_name, service, message)

    # request to all services subscribed to queue_name
    else:
        # get the endpoints_urls for services subscribed to this queue_name
        queues_endpoints = __queue_controller.search_services_by_queue_if_active(queue_name)

        response = __notification_controller.create_service_notification(queue_name, queues_endpoints, message)

    logger.info("Response obtained: {}".format(response))

    # SPECIAL CASE, WHEN A NEW OFFER IS CREATED, A USER NOTIFICATION IS CREATED TO ALERT USERS WHO ARE SUBSCRIBED TO THE
    # CATEGORY TO WHICH THE NEW OFFER BELONGS.
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
    return response


# ----------------------------USER NOTIFICATIONS----------------------------------------
# @blueprint.route('/notification/user', methods=['POST'])
@blueprint.route('/notification', methods=['POST'])
@blueprint.input(UserNotification)
@blueprint.output(Notification)
def notification_user(data):

    if not data.get('receiver_id') or not data.get("message"):
        # return jsonify({"error": "Body has to contain receiver_id and message"}), 400
        abort(400, 'Body has to contain data')

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

    return stored_notification


# @blueprint.route('/notification/', methods=['GET'])
@blueprint.route('/notification', methods=['GET'])
@blueprint.output(Notification(many=True))
def get_notifications():
    return __notification_controller.get_all_notifications()


@blueprint.route('/notification/user/<user_id>', methods=['GET'])
@blueprint.output(Notification(many=True))
def get_notification_by_userid(user_id: str):
    result = __notification_controller.get_user_notification(user_id)
    if result:
        return result
    else:
        abort(404)


# @blueprint.route('/notification/unread/', methods=['GET'])
@blueprint.route('/notification/unread', methods=['GET'])
@blueprint.output(Notification(many=True))
def get_unread_notifications():
    return __notification_controller.get_all_unread_notifications()


# @blueprint.route('/notification/user/<user_id>/unread/', methods=['GET'])
@blueprint.route('/notification/user/<user_id>/unread', methods=['GET'])
@blueprint.output(Notification(many=True))
def get_unread_notifications_by_id(user_id: str):
    return __notification_controller.get_unread_user_notification(user_id)


# @blueprint.route('/notification/<notification_id>/', methods=['GET'])
@blueprint.route('/notification/<notification_id>', methods=['GET'])
@blueprint.output(Notification)
def get_notification(notification_id: str):
    result = __notification_controller.get_notification(notification_id)
    if result:
        return result
    abort(404, "Not Found")


@blueprint.route('/notification/<notification_id>/read', methods=['PATCH'])
@blueprint.route('/notification/<notification_id>/unread', methods=['PATCH'])
@blueprint.output(Notification)
def modify_notification(notification_id: str):
    read = request.path.split('/')[-1] == 'read'
    result = __notification_controller.modify_notification(notification_id, read)
    if result:
        return result
    # return jsonify(), 404
    abort(404, "Not Found")


@blueprint.route('/notification/<notification_id>', methods=['DELETE'])
@blueprint.output(Notification)
def delete_notification(notification_id: str):
    result = __notification_controller.delete_notification(notification_id)
    if result:
        return result
    else:
        abort(404, "Not Found")
