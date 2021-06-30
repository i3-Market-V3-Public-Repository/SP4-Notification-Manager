from flask import Blueprint, request, jsonify

from src.alert_subscription.controller.subscriptions_controller import SubscriptionsController

api = Blueprint('subscriptions', __name__)
# noinspection PyTypeChecker
__controller: SubscriptionsController = None


def config(controller: SubscriptionsController):
    global __controller
    __controller = controller


@api.route('/users/subscriptions', methods=['GET'])
def get_users():
    pass


@api.route('/users/<user_id>/subscriptions', methods=['POST'])
def post_subscriptions(user_id: str):
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    result = __controller.create_subscription(user_id, request.json)

    if result is False:
        return jsonify({'error': 'Incomplete body'}), 400

    if result is None:
        return jsonify({'error': 'Already exists'}), 400

    return jsonify(result.to_json()), 200


@api.route('/users/<user_id>/subscriptions', defaults={"subscription_id": None}, methods=['GET'])
@api.route('/users/<user_id>/subscriptions/<subscription_id>', methods=['GET'])
def get_subscriptions(user_id: str, subscription_id: str):
    result = __controller.retrieve_subscription(user_id, subscription_id)

    if result is None:
        return jsonify({'error': 'Not found'}), 404

    return jsonify(result.to_json()), 200


@api.route('/users/<user_id>/subscriptions/<subscription_id>', methods=['PUT'])
def put_subscription(user_id: str, subscription_id: str):
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    result = __controller.update_subscription(user_id, subscription_id, request.json)

    if result is None:
        return jsonify({'error': 'This subscription already exists, consider deleting it'}), 400

    if result == -1:
        return jsonify({'error': 'Not found'}), 400

    return jsonify(result.to_json()), 200


@api.route('/users/<user_id>/subscriptions/<subscription_id>', methods=['DELETE'])
def delete_subscription(user_id: str, subscription_id: str):

    result = __controller.delete_subscription(user_id, subscription_id)

    if result is None:
        return jsonify({'error': 'Not found'}), 400

    return jsonify(result.to_json()), 200
