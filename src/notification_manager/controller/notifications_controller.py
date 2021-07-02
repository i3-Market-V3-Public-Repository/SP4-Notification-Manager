from src.notification_manager.storage.services_queue_storage import ServicesQueueStorage
from src.notification_manager.models.service import Service, service_to_object


class NotificationsController:
    def __init__(self, storage: ServicesQueueStorage):
        self.storage = storage

    def send_notification_service(self, data: dict):
        pass