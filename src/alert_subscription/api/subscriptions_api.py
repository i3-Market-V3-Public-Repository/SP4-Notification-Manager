from apiflask import APIBlueprint, input, output, doc, abort, fields
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


# @output(Subscription(many=True))
@output(UserSubscriptionList(many=True))
@blueprint.route('/users/subscriptions', methods=['GET'])
def get_users():
    """
    Get all users subscriptions
    :return:
    """
    result = __controller.retrieve_all()
    return jsonify(result), 200


@input(CreateSubscription)
@output(Subscription)
@blueprint.route('/users/<user_id>/subscriptions', methods=['POST'])
def post_subscriptions(user_id: str):
    """
    Create subscription to category
    :param user_id:
    :return:
    """
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    result = __controller.create_subscription(user_id, request.json)

    if result is False:
        return jsonify({'error': 'Incomplete body'}), 400

    if result is None:
        return jsonify({'error': 'Already exists subscription to category'}), 400

    return jsonify(result.to_json()), 200


@output(Subscription(many=True), example=[
    {
        "id": "82bb0248-6ce3-4fe4-9e68-6c30fe0ef41b",
        "category": "Agriculture",
        "active": True
    }
])
@blueprint.route('/users/<user_id>/subscriptions', methods=['GET'])
def get_subscriptions_by_userid(user_id: str):
    result = __controller.retrieve_subscription(user_id)
    if result is None:
        return jsonify({'error': 'Not found'}), 404

    return jsonify([s.to_json() for s in result]), 200


@output(Subscription, example={
    "id": "82bb0248-6ce3-4fe4-9e68-6c30fe0ef41b",
    "category": "Agriculture",
    "active": True
})
@blueprint.route('/users/<user_id>/subscriptions/<subscription_id>', methods=['GET'])
def get_subscriptions(user_id: str, subscription_id: str):
    """
    Get user subscription by user_id and subscription_id.
    :param user_id:
    :param subscription_id:
    :return:
    """
    result = __controller.retrieve_subscription(user_id, subscription_id)

    if result is None:
        return jsonify({'error': 'Not found'}), 404

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

@output(Subscription)
@blueprint.route('/users/<user_id>/subscriptions/<subscription_id>', methods=['DELETE'])
def delete_subscription(user_id: str, subscription_id: str):
    """
    Delete subscription by user_id and subscription_id
    :param user_id: User id of the user
    :param subscription_id: Subscription id
    :return: Subscription
    """

    result = __controller.delete_subscription(user_id, subscription_id)

    if result is None:
        return jsonify({'error': 'Not found'}), 400

    return jsonify(result.to_json()), 200


# TODO Change to PATCH instead of POST, update Postman collections and Documentation.
@output(Subscription)
@blueprint.route('/users/<user_id>/subscriptions/<subscription_id>/activate', methods=['POST'])
@blueprint.route('/users/<user_id>/subscriptions/<subscription_id>/deactivate', methods=['POST'])
def status_subscription(user_id: str, subscription_id: str):
    """
    Activate or deactivate user subscription
    :param user_id:
    :param subscription_id:
    :return:
    """
    activated = request.path.split('/')[-1] == 'activate'

    result = __controller.switch_status_subscription(user_id, subscription_id, activated)

    if result is None:
        return jsonify({'error': 'Not found'}), 400

    return jsonify(result.to_json()), 200


# @output(fields.String(many=True))
@output(UsersList)
@blueprint.route('/users/subscriptions/<category>', methods=['GET'])
def get_users_list_category(category: str):
    result = __controller.search_users_by_category(category)
    if result:
        return jsonify(result), 200
    else:
        abort(status_code=400, message="Bad Request")
