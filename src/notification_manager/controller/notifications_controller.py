from src.notification_manager.models.notification import Notification
from src.notification_manager.storage.services_queue_storage import ServicesQueueStorage
from src.notification_manager.models.service import Service, service_to_object


class NotificationsController:
    def __init__(self, storage: ServicesQueueStorage):
        self.storage = storage

    def send_notification_service(self, destiny: list, data: dict = None):
        # se crea una notification por cada destino con ¿origen?
        for d in destiny:
            notification = Notification(action="New Search Hits",
                                        status="Ok",
                                        origin="i3-market",
                                        receptor=d,
                                        data=data)
