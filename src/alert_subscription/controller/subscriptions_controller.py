import uuid

import requests

from src.alert_subscription.models.subscription import Subscription, subscription_to_object
from src.alert_subscription.storage.subscriptions_storage import SubscriptionsStorage


class SubscriptionsController:

    def __init__(self, storage: SubscriptionsStorage, web_ui: str):
        self.storage = storage
        self.web_ui = web_ui

    def retrieve_all(self):
        return self.storage.retrieve_all()

    def create_subscription(self, user_id: str, data: dict):
        if 'category' not in data.keys():
            return False

        if self.storage.search_user_subscription(user_id, data):
            return None

        subscription = Subscription(uuid.uuid4().__str__(), data.get('category'))
        stored_subscription = self.storage.insert_user_subscription(user_id, subscription.to_json())

        return subscription_to_object(stored_subscription)

    def retrieve_subscription(self, user_id: str, subscription_id: str = None):
        if subscription_id:
            retrieved_subscription = self.storage.retrieve_user_subscription(user_id, subscription_id)
        else:
            retrieved_subscription = self.storage.retrieve_all_user_subscriptions(user_id)

        if not retrieved_subscription:
            return None  # Not found

        if isinstance(retrieved_subscription, list):
            return [subscription_to_object(s) for s in retrieved_subscription]

        return subscription_to_object(retrieved_subscription)

    def update_subscription(self, user_id: str, subscription_id: str, data: dict):
        if not self.storage.retrieve_user_subscription(user_id, subscription_id):
            return -1  # Not found

        if self.storage.search_user_subscription(user_id, data):
            return None  # This subscription already exists, consider deleting it

        subscription = Subscription(subscription_id, data.get('category'), data.get('active'))
        updated_subscription = self.storage.update_user_subscription(user_id, subscription_id, subscription.to_json())

        return subscription_to_object(updated_subscription)

    def delete_subscription(self, user_id: str, subscription_id: str):
        if not self.storage.retrieve_user_subscription(user_id, subscription_id):
            return None  # Not found

        deleted_subscription = self.storage.delete_user_subscription(user_id, subscription_id)

        return subscription_to_object(deleted_subscription)

    def switch_status_subscription(self, user_id: str, subscription_id: str, activated: bool):
        subscription = self.storage.retrieve_user_subscription(user_id, subscription_id)

        if not subscription:
            return None  # Not found

        subscription = Subscription(subscription.get('id'), subscription.get('category'), activated)
        updated_subscription = self.storage.update_user_subscription(user_id, subscription_id, subscription.to_json())

        return subscription_to_object(updated_subscription)

    def search_users_by_category(self, category: str):
        result = self.storage.search_users_by_category(category)
        if len(result) > 0:
            return {"users": self.storage.search_users_by_category(category)}
        return None


