import json
import uuid

import requests

from src.notification_manager.models.notification import Notification
from src.notification_manager.models.queue_types import QueueType
from src.notification_manager.storage.notifications_storage import NotificationsStorage
from loguru import logger


class NotificationsController:

    def __init__(self, storage: NotificationsStorage, web_ui: str):
        self.storage = storage
        self.web_ui = web_ui

    @staticmethod
    def send_notification_service(self, queue_name, destiny: dict, data: dict = None):
        # se crea una notification por cada destino con ¿origen?

        if queue_name == QueueType.NEWOFFERING.value:
            for receptor_name, endpoint in destiny.items():
                logger.info("Creating a notification to {} endpoint {}".format(receptor_name, endpoint))
                notification = Notification(id=uuid.uuid4().__str__(),
                                            action="New Search Hits",
                                            status="Ok",
                                            origin="i3-market",
                                            receptor=receptor_name,
                                            data=data)
                resp = requests.post(url=endpoint, json=notification.to_json())
                logger.info("Notification service response: {}".format(resp))
        else:
            return None

    def send_notification_user(self, destiny_user_id: str, origin: str, status: str, _type: str, predefined: bool,
                               message: dict = None):
        notification = Notification(id=uuid.uuid4().__str__(),
                                    action=_type,
                                    status=status,
                                    origin=origin,
                                    receptor=destiny_user_id,
                                    data=message)
        return self.storage.insert_notification(notification.to_json())

    def get_user_notification(self, user_id):
        return self.storage.retrieve_notification_by_user(user_id)

    def get_unread_user_notification(self, user_id):
        return self.storage.retrieve_unread_notification_by_user(user_id)

    def get_all_notifications(self):
        return self.storage.retrieve_all()

    def get_all_unread_notifications(self):
        return self.storage.retrieve_all_unread()

    def get_notification(self, notification_id):
        # notifications = self.storage.retrieve_notification_by_user(user_id)
        # for notification in notifications:
        #     if notification.get('id') == notification_id:
        #         return notification
        # return None
        notification = self.storage.retrieve_notification(notification_id)
        if notification:
            return notification
        return None

    def modify_notification(self, notification_id, read):
        return self.storage.read_notification(notification_id, read)

    def delete_notification(self, notification_id):
        return self.storage.delete_notification(notification_id)
