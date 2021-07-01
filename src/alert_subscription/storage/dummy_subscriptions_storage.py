import json
import os

from loguru import logger

from src.alert_subscription.storage.subscriptions_storage import SubscriptionsStorage


class DummySubscriptionsStorage(SubscriptionsStorage):

    def __init__(self, path):
        self.path = path

        if not os.path.exists(self.path):
            self.__write_dummy_file(data={})

        self.storage = self.__read_dummy_file()

        logger.info('Dummy Storage enabled')

    def retrieve_all(self):
        return self.storage

    def search_user_subscription(self, user_id: str, data: dict):
        if user_id not in self.storage.keys():
            return None   # User Not found

        for subscription in self.storage.get(user_id):
            if subscription == data:
                return subscription

        return None  # Subscription Not found

    def insert_user_subscription(self, user_id: str, subscription: dict):
        # if the user does not exist, it is created
        if user_id not in self.storage.keys():
            self.storage[user_id] = []

        # the subscription is added to the user
        self.storage[user_id].append(subscription)
        self.__write_dummy_file(self.storage)

        return subscription

    def retrieve_all_user_subscriptions(self, user_id: str):
        return self.storage.get(user_id)

    def retrieve_user_subscription(self, user_id: str, subscription_id: str):
        if user_id not in self.storage.keys():
            return None  # User Not found

        # subscription is searched by the user
        for s in self.storage.get(user_id):
            if s.get('id') == subscription_id:
                return s

        return None  # Subscription Not found

    def update_user_subscription(self, user_id: str, subscription_id: str, data: dict):
        if user_id not in self.storage.keys():
            return None  # User Not found

        for i in list(range(0, len(self.storage.get(user_id)))):
            subscription = self.storage.get(user_id)[i]
            if subscription.get('id') == subscription_id:
                self.storage[user_id][i] = data
                self.__write_dummy_file(self.storage)
                return data

        return None  # Subscription Not found

    def delete_user_subscription(self, user_id: str, subscription_id: str):
        if user_id not in self.storage.keys():
            return None  # User Not found

        index = None
        for i in list(range(0, len(self.storage.get(user_id)))):
            subscription = self.storage.get(user_id)[i]
            if subscription.get('id') == subscription_id:
                index = i
                break

        if index:
            return self.storage[user_id].pop(index)

        return None  # Subscription Not found

    def __read_dummy_file(self):
        with open(self.path, 'r') as file:
            return json.load(file)

    def __write_dummy_file(self, data: dict):
        with open(self.path, 'w') as file:
            return json.dump(data, file, indent=2)
