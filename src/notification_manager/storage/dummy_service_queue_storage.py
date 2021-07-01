import json
import os

from loguru import logger

from src.notification_manager.storage.services_queue_storage import ServicesQueueStorage


class DummyServiceQueueStorage(ServicesQueueStorage):

    def __init__(self, path):
        self.path = path

        if not os.path.exists(self.path):
            self.__write_dummy_file(data={})

        self.storage = self.__read_dummy_file()

        logger.info('Dummy Storage enabled')

    def retrieve_all(self):
        return self.storage

    ####################################################################################################################
    # SERVICES METHODS
    ####################################################################################################################
    def insert_service(self, service: dict):
        # if the user does not exist, it is created
        found = next((item for item in self.storage if item["id"] == service.get('id')), None)
        if found:
            return self.update_service(service)
        else:
            # the service is added to the user
            self.storage.append(service)
            self.__write_dummy_file(self.storage)
            return service

    def retrieve_service(self, service_id: dict):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                return existing_service
        return None

    def update_service(self, service: dict):
        for i in list(range(0, len(self.storage))):
            existing_service = self.storage[i]
            if existing_service.get('id') == service.get('id'):
                self.storage[i] = service
                self.__write_dummy_file(self.storage)
                return service
        return None  # Service Not found

    def delete_service(self, service_id):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                self.storage.remove(existing_service)
                return True
        return False
        #for i in list(range(0, len(self.storage))):
        #    existing_service = self.storage[i]
        #    if existing_service.get('id') == service_id:
        #        # del self.storage[i]

    ####################################################################################################################
    # QUEUES METHODS
    ####################################################################################################################
    def retrieve_all_service_queues(self, service_id: str):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                return existing_service.queues

    def retrieve_service_queue(self, service_id: str, queue_id: str):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                for queue in existing_service.get('queue'):
                    if queue.get('id') == queue_id:
                        return queue
        return None  # queue Not found

    def insert_service_queue(self, service_id: str, queue: dict):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                list(existing_service.get('queue')).append(queue)
                return queue
        return None

    def update_service_queue(self, service_id: str, queue: dict):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                existing_queue = existing_service.get('queue')
                for i in list(range(0, len(existing_queue))):
                    if queue.get('id') == existing_queue[i].get('id'):
                        existing_queue[i] = queue

    def delete_service_queue(self, service_id: str, queue_id: str):
        for existing_services in self.storage:
            if existing_services.get('id') == service_id:
                queue = existing_services.get('queue')
                for existing_queue in queue:
                    if existing_queue.get('id') == queue_id:
                        queue.remove()
                        return True
        return None  # queue not found

    def __read_dummy_file(self):
        with open(self.path, 'r') as file:
            return json.load(file)

    def __write_dummy_file(self, data: dict):
        with open(self.path, 'w') as file:
            return json.dump(data, file, indent=2)
