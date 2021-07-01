import uuid

from src.notification_manager.storage.services_queue_storage import ServicesQueueStorage
from src.notification_manager.models.service import Service, service_to_object
from src.notification_manager.models.queue import Queue


class QueueController:

    def __init__(self, storage: ServicesQueueStorage):
        self.storage = storage

    def retrieve_all(self):
        return [service_to_object(s) for s in self.storage.retrieve_all()]

    def create_service(self, data: dict):
        if 'name' not in data.keys():
            return False
        service = Service(uuid.uuid4().__str__(), data.get('name'), data.get('endpoint'))
        stored_service = self.storage.insert_service(service.to_json())

    def retrieve_service(self):
        pass

    def update_service(self):
        pass

    def delete_service(self):
        pass

    def create_queue(self, data: dict):
        if 'name' not in data.keys():
            return False
        queue = Queue(uuid.uuid4().__str__(), data.get('name'), data.get('endpoint'))
        return queue
    def get_queue(self):
        pass

    def update_queue(self):
        pass

    def switch_status_queue(self, service_id: str, queue_id: str, activated: bool):
        pass
