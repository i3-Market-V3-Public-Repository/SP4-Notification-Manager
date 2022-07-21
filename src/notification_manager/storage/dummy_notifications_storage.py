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

        logger.info('Dummy Storage enabled at: {}'.format(self.path))

    def retrieve_all(self):
        return self.storage

    def retrieve_all_unread(self):
        unread_notifications = []
        all_notifications = self.retrieve_all()
        for notification in all_notifications:
            if notification.get('unread'):
                unread_notifications.append(notification)
        return unread_notifications

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
        return {}

    def retrieve_notification_by_user(self, user_id: str):
        return_notifications = []
        for notification in self.storage:
            if notification.get('receptor') == user_id:
                return_notifications.append(notification)
        return return_notifications

    def retrieve_unread_notification_by_user(self, user_id: str):
        unread_notifications = []
        for notification in self.retrieve_notification_by_user(user_id):
            if notification.get('unread'):
                unread_notifications.append(notification)
        return unread_notifications

    def modify_read_notification(self, notification_id, read: bool):
        notif = self.retrieve_notification(notification_id)
        if notif:
            notif["unread"] = not read
            self.__write_dummy_file()
            return notif
        else:
            return None
        # for i in list(range(0, len(self.storage))):
        #     existing_service = self.storage[i]
        #     if existing_service.get('id') == notification_id:
        #         existing_service["unread"] = not read
        #         self.__write_dummy_file()
        #         return existing_service
        #     return None  # Service Not found

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

        return None  # Notification Not found

    def __read_dummy_file(self):
        with open(self.path, 'r') as file:
            return json.load(file)

    def __write_dummy_file(self):
        with open(self.path, 'w+') as file:
            return json.dump(self.storage, file, indent=2)
