from src.notification_manager.storage.services_queue_storage import ServicesQueueStorage
from src.notification_manager.models.service import Service, service_to_object


class NotificationsController:
    def __init__(self, storage: ServicesQueueStorage):
        self.storage = storage

    def retrieve_all(self):
        """
        Return all the services with their queues
        :return:
        """
        return [service_to_object(s) for s in self.storage.retrieve_all()]

    def create_service(self):
        pass

    def get_service(self):
        pass

    def update_service(self):
        pass
