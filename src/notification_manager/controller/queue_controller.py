import uuid

from src.notification_manager.storage.services_queue_storage import ServicesQueueStorage
from src.notification_manager.models.queue import Queue


class QueueController:

    def __init__(self, storage: ServicesQueueStorage):
        self.storage = storage

    def create_queue(self, data: dict):
        if 'name' not in data.keys():
            return False
        queue = Queue(uuid.uuid4().__str__(), data.get('name'), data.get('endpoint'))
        self.storage.create_service()
        return queue

    def get_queue(self):
        pass

    def update_queue(self):
        pass
