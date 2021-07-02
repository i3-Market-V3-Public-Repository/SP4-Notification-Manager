import uuid

from src.notification_manager.storage.services_queue_storage import ServicesQueueStorage
from src.notification_manager.models.service import Service, service_to_object
from src.notification_manager.models.queue import Queue, queue_to_object


class QueueController:

    def __init__(self, storage: ServicesQueueStorage):
        self.storage = storage

    def retrieve_all(self):
        return self.storage.retrieve_all()

    def create_service(self, data: dict):
        if 'name' not in data.keys():
            return False

        service = Service(uuid.uuid4().__str__(), data.get('name'), data.get('endpoint'))
        stored_service = self.storage.insert_service(service.to_json())

        if stored_service:
            return service_to_object(stored_service)

    def retrieve_service(self, service_id: str):
        service = self.storage.retrieve_service(service_id)
        if not service:
            return None
        if isinstance(service, dict):
            service_to_object(service)

    def update_service(self, service_id: str, data: dict):
        # TODO i dont like this method change it
        if not self.storage.retrieve_service(service_id):
            return -1  # not found
        else:
            updated_service = self.storage.update_service(data)
            if not updated_service:
                return None  # service not found
            else:
                return service_to_object(updated_service)

    def delete_service(self, service_id):
        deleted_service = self.storage.delete_service(service_id)
        if not deleted_service:
            return None
        else:
            return service_to_object(deleted_service)

    def create_queue(self, service_id: str, data: dict):
        if 'name' not in data.keys():
            return False
        queue = Queue(uuid.uuid4().__str__(), data.get('name'), data.get('endpoint'))
        stored_queue = self.storage.insert_service_queue(service_id, queue.to_json())
        return queue_to_object(stored_queue)

    def retrieve_service_queues(self, service_id: str, queue_id: str = None):
        if queue_id:
            retrieved_queue = self.storage.retrieve_service_queue(service_id, queue_id)
        else:
            retrieved_queue = self.storage.retrieve_all_service_queues(service_id)
        if not retrieved_queue:
            return None
        else:
            if isinstance(retrieved_queue, list):
                retrieved_queue = [queue_to_object(s) for s in retrieved_queue]
            return queue_to_object(retrieved_queue)

    def update_queue(self, service_id: str, queue_id:str, data: dict):
        if not self.storage.retrieve_service_queue(service_id, queue_id):
            return -1
        queue = self.storage.update_service_queue(service_id,data)
        if queue:
            return queue_to_object(queue)
        return None

    def delete_queue(self, service_id: str, queue_id:str):
        if not self.storage.retrieve_service_queue(service_id, queue_id):
            return None  # Not found
        deleted_queue = self.storage.delete_service_queue(service_id,queue_id)
        return queue_to_object(deleted_queue)

    def switch_status_queue(self, service_id: str, queue_id: str, activated: bool):
        queue = self.storage.retrieve_service_queue(service_id, queue_id)
        if not queue:
            return None  # not found
        queue = Queue(queue.get('id'), queue.get('name'), queue.get('endpoint'), activated)
        updated_queue = self.storage.update_service_queue(service_id, queue.to_json())
        return queue_to_object(updated_queue)
