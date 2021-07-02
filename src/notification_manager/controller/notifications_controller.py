import requests

from src.notification_manager.models.notification import Notification
from src.notification_manager.models.queue_types import QueueType


class NotificationsController:

    def send_notification_service(self, queue_name, destiny: list, data: dict = None):
        # se crea una notification por cada destino con ¿origen?

        if queue_name == QueueType.NEWOFFERING.value:

            for d in destiny:
                endpoint = d.get('endpoint')
                notification = Notification(action="New Search Hits",
                                            status="Ok",
                                            origin="i3-market",
                                            receptor=d.get('name'),
                                            data=data)
                requests.post(url=endpoint, json=notification.to_json())
        else:
            return None
