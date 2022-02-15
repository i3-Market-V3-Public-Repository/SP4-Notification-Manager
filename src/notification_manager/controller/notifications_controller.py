import json
import uuid

import requests

from src.notification_manager.models.notification import Notification, notification_to_object
from src.notification_manager.models.queue_types import QueueType
from src.notification_manager.storage.notifications_storage import NotificationsStorage
from loguru import logger


class NotificationsController:

    def __init__(self, storage: NotificationsStorage, web_ui: str):
        self.storage = storage
        self.web_ui = web_ui

    def create_service_notification(self, queue_name, queues, message):
        # create the notification and send to them
        return self.send_notification_service(queue_name, queues, message)

    @staticmethod
    def send_notification_service(queue_name, destiny: dict, data: dict = None):
        response = []
        for receptor_name, endpoint in destiny.items():
            logger.info("Creating a notification to {} endpoint {}".format(receptor_name, endpoint))
            notification = None
            if queue_name == QueueType.NEWOFFERING.value:
                notification = Notification.new_offering_notification(receptor_name=receptor_name, data=data)

            elif queue_name == QueueType.UPDATEOFFERING.value:
                notification = Notification.update_offering_notification(receptor_name=receptor_name, data=data)

            # Agreements are currently sent as user notifications
            # elif queue_name == QueueType.AGREEMENTUPDATE.value:
            #     pass
            # elif queue_name == QueueType.AGREEMENTACCEPTED.value:
            #     pass
            # elif queue_name == QueueType.AGREEMENTPENDING.value:
            #     pass
            # elif queue_name == QueueType.AGREEMENTREJECTED.value:
            #     pass
            # elif queue_name == QueueType.AGREEMENTTERMINATION.value:
            #     pass

            # Only this is used, sent to conflict resolution.
            elif queue_name == QueueType.AGREEMENTCLAIM.value:
                pass

            if notification is not None:
                resp = requests.post(url=endpoint, json=notification.to_json())
                response.append(
                        {"destiny": receptor_name, "response": resp.status_code})
                #logger.info("Notification service response: {}".format(resp))

        return response

    def send_notification_user(self, destiny_user_id: str, origin: str, status: str, _type: str, predefined: bool,
                               message: dict = None):

        notification = Notification(_id=uuid.uuid4().__str__(),
                                    action=_type,
                                    status=status,
                                    origin=origin,
                                    receptor=destiny_user_id,
                                    data=message)
        return self.storage.insert_notification(notification.to_json())

    def get_user_notification(self, user_id):
        return [notification_to_object(notification).to_json() for notification in self.storage.retrieve_notification_by_user(user_id)]

    def get_unread_user_notification(self, user_id):
        return [notification_to_object(notification).to_json() for notification in self.storage.retrieve_unread_notification_by_user(user_id)]

    def get_all_notifications(self):
        return [notification_to_object(notification).to_json() for notification in self.storage.retrieve_all()]

    def get_all_unread_notifications(self):
        return [notification_to_object(notification).to_json() for notification in self.storage.retrieve_all_unread()]

    def get_notification(self, notification_id):
        # notifications = self.storage.retrieve_notification_by_user(user_id)
        # for notification in notifications:
        #     if notification.get('id') == notification_id:
        #         return notification
        # return None
        notification = self.storage.retrieve_notification(notification_id)
        if notification:
            return notification_to_object(notification).to_json()
        return None

    def modify_notification(self, notification_id, read):
        notif = self.storage.read_notification(notification_id, read)
        if notif:
            return notification_to_object(notif).to_json()
        return notif

    def delete_notification(self, notification_id):
        deleted_notif = self.storage.delete_notification(notification_id)
        if deleted_notif:
            return notification_to_object(deleted_notif).to_json()
        return deleted_notif  # result is None
