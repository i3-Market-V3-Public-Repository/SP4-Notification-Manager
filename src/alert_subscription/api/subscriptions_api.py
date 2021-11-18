from apiflask import output, APIBlueprint, input, output
from flask import Blueprint, request, jsonify
from loguru import logger

from src.alert_subscription.controller.subscriptions_controller import SubscriptionsController
from src.alert_subscription.models.AlertsSwaggerModelScheme import SubscriptionList, Subscription, CreateSubscription, \
    UserSubscriptionList

blueprint = APIBlueprint('subscriptions', __name__, url_prefix='/api/v1/')
# noinspection PyTypeChecker
__controller: SubscriptionsController = None


def config(controller: SubscriptionsController):
    global __controller
    __controller = controller


# Just for testing, hide request
# @blueprint.route('/notify', methods=['POST'])
def notify():
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    category = request.json.get('category')

    __controller.search_users_by_subscription(category, message=request.json)

    return jsonify(), 200


@output(UserSubscriptionList, example={
  "user001": [
    {
      "id": "9c551aec-0049-41c0-b4d3-1065cad985bb",
      "category": "category1",
      "active": True
    },
    {
      "id": "3a275fc8-b231-4c42-ae34-8f90db8e6a12",
      "category": "category2",
      "active": True
    }
  ],
  "asd2": [
    {
      "id": "d9ead632-fce5-443c-afe8-46f470f1a74f",
      "category": "category2",
      "active": False
    }
  ]
})
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


@output(SubscriptionList, example=[
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


# @api.route('/users/<user_id>/subscriptions/<subscription_id>', methods=['PUT'])
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
    :param user_id:
    :param subscription_id:
    :return:
    """

    result = __controller.delete_subscription(user_id, subscription_id)

    if result is None:
        return jsonify({'error': 'Not found'}), 400

    return jsonify(result.to_json()), 200


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
