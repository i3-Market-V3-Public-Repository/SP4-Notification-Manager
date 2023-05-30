import json
import uuid

import requests

from src.notification_manager.models.notification import Notification, notification_to_object
from src.notification_manager.models.queue_types import QueueType
from src.notification_manager.storage.notifications_storage import NotificationsStorage
from loguru import logger
from requests.adapters import HTTPAdapter, Retry

retry_strategy = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"],
    backoff_factor=1
)
session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=retry_strategy))


class NotificationsController:

    def __init__(self, storage: NotificationsStorage, web_ui: str):
        self.storage = storage
        self.web_ui = web_ui

    def create_service_notification(self, queue_name, queues, message):
        # create the notification and send to them
        return self.send_notification_service(queue_name, queues, message)

    @staticmethod
    def create_specific_service_notification(queue_name, receptor_name, data) -> Notification:
        notification = None
        if queue_name == QueueType.NEWOFFERING.value:
            notification = Notification.new_offering_notification(receptor_name=receptor_name, data=data)

        elif queue_name == QueueType.UPDATEOFFERING.value:
            notification = Notification.update_offering_notification(receptor_name=receptor_name, data=data)

        elif queue_name == QueueType.AGREEMENTUPDATE.value:
            notification = Notification.agreement_notification(status="Update", data=data)

        elif queue_name == QueueType.AGREEMENTACCEPTED.value:
            notification = Notification.agreement_notification(status="Accepted", data=data)

        elif queue_name == QueueType.AGREEMENTPENDING.value:
            notification = Notification.agreement_notification(status="Pending", data=data)

        elif queue_name == QueueType.AGREEMENTREJECTED.value:
            notification = Notification.agreement_notification(status="Rejected", data=data)

        elif queue_name == QueueType.AGREEMENTTERMINATION.value:
            notification = Notification.agreement_notification(status="Termination", data=data)

        elif queue_name == QueueType.AGREEMENTCLAIM.value:
            notification = Notification.agreement_notification(status="Claim", data=data)

        elif queue_name == QueueType.AGREEMENTPENALTYCHOICES.value:
            notification = Notification.agreement_notification(status="PenaltyChoices", data=data)

        elif queue_name == QueueType.AGREEMENTPROPOSEPENALTY.value:
            notification = Notification.agreement_notification(status="ProposePenalty", data=data)

        elif queue_name == QueueType.AGREEMENTAGREEONPENALTY.value:
            notification = Notification.agreement_notification(status="AgreeOnPenalty", data=data)

        elif queue_name == QueueType.AGREEMENTREJECTPENALTY.value:
            notification = Notification.agreement_notification(status="RejectPenalty", data=data)

        elif queue_name == QueueType.AGREEMENTTERMINATIONPROPOSAL.value:
            notification = Notification.agreement_notification(status="TerminationProposal", data=data)

        elif queue_name == QueueType.AGREEMENTTERMINATIONREJECTION.value:
            notification = Notification.agreement_notification(status="TerminationRejection", data=data)

        elif queue_name == QueueType.CONSENTGIVEN.value:
            notification = Notification.consent_notification(status='Given', data=data)

        elif queue_name == QueueType.CONSENTREVOKED.value:
            notification = Notification.consent_notification(status='Revoked', data=data)

        return notification

    def send_notification_service(self, queue_name, destiny: dict, data: dict = None):
        response = []
        for receptor_name, endpoint in destiny.items():
            logger.info("Creating a notification to {} endpoint {}".format(receptor_name, endpoint))
            notification = self.create_specific_service_notification(queue_name, receptor_name, data)

            if notification is not None:
                try:

                    resp = session.post(url=endpoint, json=notification.to_json())
                    if resp:
                        response.append(
                            {"destiny": receptor_name, "response": resp.status_code})

                except BaseException as e:
                    logger.error(f"Error in request, log:\n {e}")
                    response.append(
                        {"destiny": receptor_name, "response": 'error'})

                # logger.debug("Notification service response: {}".format(resp))

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
        notif = self.storage.modify_read_notification(notification_id, read)
        if notif:
            return notification_to_object(notif).to_json()
        return notif

    def delete_notification(self, notification_id):
        deleted_notif = self.storage.delete_notification(notification_id)
        if deleted_notif:
            return notification_to_object(deleted_notif).to_json()
        return deleted_notif  # result is None
