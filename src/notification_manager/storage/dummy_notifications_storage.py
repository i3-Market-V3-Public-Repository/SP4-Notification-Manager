import json
import os

from loguru import logger

from src.notification_manager.storage.notifications_storage import NotificationsStorage


class DummyNotificationsStorage(NotificationsStorage):

    def __init__(self, path):
        self.path = path
        self.storage = []

        if not os.path.exists(self.path):
            self.__write_dummy_file()

        self.storage = self.__read_dummy_file()

        logger.info('Dummy Storage enabled')

    def retrieve_all(self):
        return self.storage

    ####################################################################################################################
    # NOTIFICATIONS METHODS
    ####################################################################################################################
    def insert_notification(self, notification: dict):
        self.storage.append(notification)
        self.__write_dummy_file()
        return notification

    def retrieve_notification(self, notification_id: dict):
        for existing_notification in self.storage:
            if existing_notification.get('id') == notification_id:
                return existing_notification
        return None

    def retrieve_notification_by_user(self, user_id: str):
        return_notifications = []
        for notification in self.storage:
            if notification.get('receptor') == user_id:
                return_notifications.append(notification)
        return return_notifications

    def mark_as_read_notification(self, notification_id: str):
        for i in list(range(0, len(self.storage))):
            existing_service = self.storage[i]
            if existing_service.get('id') == notification_id:
                existing_service["unread"] = False
                self.__write_dummy_file()
                return existing_service
        return None  # Service Not found

    def mark_as_unread_notification(self, notification_id: str):
        for i in list(range(0, len(self.storage))):
            existing_service = self.storage[i]
            if existing_service.get('id') == notification_id:
                existing_service["unread"] = True
                self.__write_dummy_file()
                return existing_service
        return None  # Service Not found

    def delete_notification(self, notification_id):
        index = None
        for i in list(range(0, len(self.storage))):
            if self.storage[i].get('id') == notification_id:
                index = i
                break

        if index is not None:
            deleted_service = self.storage.pop(index)
            self.__write_dummy_file()
            return deleted_service

        return None  # Service Not found

    def __read_dummy_file(self):
        with open(self.path, 'r') as file:
            return json.load(file)

    def __write_dummy_file(self):
        with open(self.path, 'w') as file:
            return json.dump(self.storage, file, indent=2)
