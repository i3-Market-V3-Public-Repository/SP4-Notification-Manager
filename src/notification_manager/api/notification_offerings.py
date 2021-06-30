from flask import Blueprint

from src.alert_subscription.storage.subscriptions_storage import SubscriptionsStorage

api = Blueprint('queues', __name__)
# noinspection PyTypeChecker
__adapter: SubscriptionsStorage = None


def config_database(adapter: SubscriptionsStorage):
    global __adapter
    __adapter = adapter


@api.route('/notification/service', methods=['POST'])
def notification_service():
    pass


@api.route('/notification/user', methods=['POST'])
def notification_service():
    pass
