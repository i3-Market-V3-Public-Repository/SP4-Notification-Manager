from apiflask import APIBlueprint, abort
from flask import request, jsonify
from loguru import logger

from src.alert_subscription.controller.subscriptions_controller import SubscriptionsController
from src.alert_subscription.models.AlertsSwaggerModelScheme import Subscription, CreateSubscription, \
    UserSubscriptionList, UsersList

blueprint = APIBlueprint('subscriptions', __name__, url_prefix='/api/v1/')
# noinspection PyTypeChecker
__controller: SubscriptionsController = None


def config(controller: SubscriptionsController):
    global __controller
    __controller = controller


@blueprint.route('/users/subscriptions', methods=['GET'])
@blueprint.output(UserSubscriptionList(many=True))
def get_users():
    """
    Get all users subscriptions
    :return:
    """
    result = __controller.retrieve_all()
    return jsonify(result), 200


@blueprint.route('/users/<user_id>/subscriptions', methods=['POST'])
@blueprint.input(CreateSubscription)
@blueprint.output(Subscription)
def post_subscriptions(user_id: str):
    """
    Create subscription to category
    :param user_id:
    :return:
    """
    if not request.json:
        abort(400, 'Empty Body')

    result = __controller.create_subscription(user_id, request.json)

    if result is False:
        abort(400, 'Incomplete Body')

    if result is None:
        abort(400, 'Already exists subscription to category')

    return jsonify(result.to_json()), 200


@blueprint.route('/users/<user_id>/subscriptions', methods=['GET'])
@blueprint.output(Subscription(many=True), example=[
    {
        "id": "82bb0248-6ce3-4fe4-9e68-6c30fe0ef41b",
        "category": "Agriculture",
        "active": True
    }
])
def get_subscriptions_by_userid(user_id: str):
    result = __controller.retrieve_subscription(user_id)
    if result is None:
        # return jsonify({'error': 'Not found'}), 404
        abort(404, "Not Found")

    return jsonify([s.to_json() for s in result]), 200


@blueprint.route('/users/<user_id>/subscriptions/<subscription_id>', methods=['GET'])
@blueprint.output(Subscription, example={
    "id": "82bb0248-6ce3-4fe4-9e68-6c30fe0ef41b",
    "category": "Agriculture",
    "active": True
})
def get_subscriptions(user_id: str, subscription_id: str):
    """
    Get user subscription by user_id and subscription_id.
    :param user_id:
    :param subscription_id:
    :return:
    """
    result = __controller.retrieve_subscription(user_id, subscription_id)

    if result is None:
        abort(404, "Not Found")

    return jsonify(result.to_json()), 200


# @api.route('/users/<user_id>/subscriptions/<subscription_id>', methods=['PATCH'])
# def put_subscription(user_id: str, subscription_id: str):
#     if not request.json:
#         return jsonify({'error': 'Empty body'}), 400
#
#     result = __controller.update_subscription(user_id, subscription_id, request.json)
#
#     if result is None:
#         return jsonify({'error': 'This subscription already exists, consider deleting it'}), 400
#
#     if result == -1:
#         return jsonify({'error': 'Not found'}), 400
#
#     return jsonify(result.to_json()), 200

@blueprint.route('/users/<user_id>/subscriptions/<subscription_id>', methods=['DELETE'])
@blueprint.output(Subscription)
def delete_subscription(user_id: str, subscription_id: str):
    """
    Delete subscription by user_id and subscription_id
    :param user_id: User id of the user
    :param subscription_id: Subscription id
    :return: Subscription
    """

    result = __controller.delete_subscription(user_id, subscription_id)

    if result is None:
        abort(404, 'Not Found')

    return jsonify(result.to_json()), 200


@blueprint.route('/users/<user_id>/subscriptions/<subscription_id>/activate', methods=['PATCH'])
@blueprint.route('/users/<user_id>/subscriptions/<subscription_id>/deactivate', methods=['PATCH'])
@blueprint.output(Subscription)
def switch_status_subscription(user_id: str, subscription_id: str):
    """
    Activate or deactivate user subscription

    :param user_id: string
    :param subscription_id: string
    :return: subscription modified
    """
    activated = request.path.split('/')[-1] == 'activate'

    result = __controller.switch_status_subscription(user_id, subscription_id, activated)

    if result is None:
        abort(404, 'Not Found')

    return jsonify(result.to_json()), 200


# TODO ¿add /category/<category> to path to distinguish category?
@blueprint.route('/users/subscriptions/<category>', methods=['GET'])
@blueprint.output(UsersList)
def get_users_list_category(category: str):
    """
    Returns a json containing a list of users subscribed to that category

    :param category: string
    :return: {'users':['user1','user2']}
    """
    result = __controller.search_users_by_category(category)
    if result:
        return jsonify(result), 200
    return abort(404, "Not Found")
