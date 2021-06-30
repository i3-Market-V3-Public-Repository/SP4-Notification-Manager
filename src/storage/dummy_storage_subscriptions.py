import json
import os

from loguru import logger

from src.storage.storage import Storage


class DummyStorageSubscriptions(Storage):

    def __init__(self, path):
        self.path = path

        if not os.path.exists(self.path):
            self.__write_dummy_file(data={})

        self.storage = self.__read_dummy_file()

        logger.info('Dummy Storage enabled')

    def create_user_subscription(self, user_id: str, subscription: dict):
        # si el usuario no existe, se crea su key
        if user_id not in self.storage.keys():
            self.storage[user_id] = []

        # buscamos si existe el id de la suscripción
        exists_subscription = False
        for s in self.storage[user_id]:
            if s.get('id') == subscription.get('id'):
                exists_subscription = True
                break

        # si no existe creamos la suscripción y la devolvemos
        if not exists_subscription:
            self.storage[user_id].append(subscription)
            self.__write_dummy_file(self.storage)
            return subscription

        return None

    def retrieve_all_user_subscriptions(self, user_id: str):
        return self.storage[user_id]

    def retrieve_user_subscription(self, user_id: str, subscription_id: str):
        # Buscamos la subscripción por id
        for s in self.storage[user_id]:
            if s.get('id') == subscription_id:
                return s

        return None

    def update_user_subscription(self, user_id: str, subscription_id: str, subscription: dict):
        for s in self.storage[user_id]:
            if s.get('id') == subscription_id:
                s = subscription
                self.__write_dummy_file(self.storage)
                return s

        return None

    def delete_user_subscription(self, user_id: str, subscription_id: str):
        index = None
        for i in list(range(0, len(self.storage[user_id]))):
            if self.storage[user_id][i].get('id') == subscription_id:
                index = i
                break

        if index:
            return self.storage[user_id].pop(index)

        return None

    def __read_dummy_file(self):
        with open(self.path, 'r') as file:
            return json.load(file)

    def __write_dummy_file(self, data: dict):
        with open(self.path, 'w') as file:
            return json.dump(data, file)
