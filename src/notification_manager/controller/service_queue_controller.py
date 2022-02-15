import uuid

from src.notification_manager.models.queue_types import QueueType
from src.notification_manager.storage.services_queue_storage import ServicesQueueStorage
from src.notification_manager.models.service import Service, service_to_object
from src.notification_manager.models.queue import Queue, queue_to_object


class QueueController:

    def __init__(self, storage: ServicesQueueStorage):
        self.storage = storage

    def retrieve_all(self):
        return [service_to_object(service).to_json() for service in self.storage.retrieve_all()]

    ####################################################################################################################
    # SERVICES API
    ####################################################################################################################
    def create_service(self, data: dict):
        if 'name' not in data.keys():
            return False

        service = Service(
            _id=uuid.uuid4().__str__(),
            market_id=data.get('marketId'),
            name=data.get('name'),
            endpoint=data.get('endpoint')
        )
        stored_service = self.storage.insert_service(service.to_json())

        if stored_service:
            return service_to_object(stored_service)

    def retrieve_service(self, service_id: str):
        service = self.storage.retrieve_service(service_id)
        # if not service:
        #     return None
        if isinstance(service, dict):
            return service_to_object(service)
        return None

    # def update_service(self, service_id: str, data: dict):
    #
    #     if not self.storage.retrieve_service(service_id):
    #         return -1  # not found
    #     else:
    #         updated_service = self.storage.update_service(data)
    #         if not updated_service:
    #             return None  # service not found
    #         else:
    #             return service_to_object(updated_service)

    def delete_service(self, service_id):
        deleted_service = self.storage.delete_service(service_id)
        if not deleted_service:
            return None
        else:
            return service_to_object(deleted_service)

    ####################################################################################################################
    # QUEUES API
    ####################################################################################################################
    def create_queue(self, service_id: str, data: dict):
        if 'name' not in data.keys():
            return False
        queue_name = data.get('name')

        if QueueType.is_valid(queue_name):
            queue = Queue(uuid.uuid4().__str__(), queue_name, data.get('endpoint'))
            stored_queue = self.storage.insert_service_queue(service_id, queue.to_json())
            if stored_queue:
                return queue_to_object(stored_queue)
            else:
                return None
        return -1

    def retrieve_service_queues(self, service_id: str, queue_id: str = None):
        if queue_id:
            retrieved_queue = self.storage.retrieve_service_queue(service_id, queue_id)
        else:
            retrieved_queue = self.storage.retrieve_all_service_queues(service_id)

        if isinstance(retrieved_queue, list):
            return [queue_to_object(s) for s in retrieved_queue]

        if retrieved_queue:
            return queue_to_object(retrieved_queue)

    # def update_queue(self, service_id: str, queue_id: str, data: dict):
    #     if not self.storage.retrieve_service_queue(service_id, queue_id):
    #         return -1
    #     queue = self.storage.update_service_queue(service_id,data)
    #     if queue:
    #         return queue_to_object(queue)
    #     return None

    def delete_queue(self, service_id: str, queue_id: str):
        if not self.storage.retrieve_service_queue(service_id, queue_id):
            return None  # Not found

        deleted_queue = self.storage.delete_service_queue(service_id, queue_id)
        if deleted_queue:
            return queue_to_object(deleted_queue)

    def switch_status_queue(self, service_id: str, queue_id: str, activated: bool):
        queue = self.storage.retrieve_service_queue(service_id, queue_id)

        if not queue:
            return None  # not found

        queue = Queue(queue.get('id'), queue.get('name'), queue.get('endpoint'), activated)
        updated_queue = self.storage.update_service_queue(service_id, queue.to_json())
        return queue_to_object(updated_queue)

    def search_services_by_queue_if_active(self, queue_name: str):
        return self.storage.get_service_endpoint_by_queue_name_if_active(queue_name)

    def search_services_by_market_id_if_active(self, market_id: str, queue_name: str):
        return self.storage.get_service_endpoint_by_market_id_if_active(market_id, queue_name)
