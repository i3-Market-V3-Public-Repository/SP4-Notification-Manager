from flask import Blueprint

from src.alert_subscription.storage.subscriptions_storage import SubscriptionsStorage

api = Blueprint('subscriptions', __name__)
# noinspection PyTypeChecker
__adapter: SubscriptionsStorage = None


def config_database(adapter: SubscriptionsStorage):
    global __adapter
    __adapter = adapter


# Expenses
@api.route('/users/{user_id}/subscriptions', methods=['POST'])
def post_subscriptions(user_id: str):
    pass


@api.route('/users/{user_id}/subscriptions', defaults={"subscription_id": None}, methods=['GET'])
@api.route('/users/{user_id}/subscriptions/<subscription_id>', methods=['GET'])
def get_subscriptions(user_id: str, subscription_id: str):
    pass


@api.route('/users/{user_id}/subscriptions/<subscription_id>', methods=['DELETE'])
def delete_subscription(user_id: str, subscription_id: str):
    pass


@api.route('/users/{user_id}/subscriptions/<subscription_id>', methods=['PUT'])
def put_subscription(user_id: str, subscription_id: str):
    pass
