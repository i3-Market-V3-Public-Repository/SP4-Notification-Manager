import json
import os

from loguru import logger

from src.notification_manager.storage.services_queue_storage import ServicesQueueStorage


class DummyServiceQueueStorage(ServicesQueueStorage):

    def __init__(self, path):
        self.path = path
        self.storage = []

        if not os.path.exists(self.path):
            self.__write_dummy_file()

        self.storage = self.__read_dummy_file()

        logger.info('Dummy Storage enabled')

    def retrieve_all(self):
        return self.storage

    ####################################################################################################################
    # SERVICES METHODS
    ####################################################################################################################
    def insert_service(self, service: dict):
        # if the user does not exist, it is created
        found = next((item for item in self.storage if item["name"] == service.get('name')), None)
        if found:
            return None  # Duplicated, maybe update
            # return self.update_service(service)
        else:
            # the service is added to the user
            self.storage.append(service)
            self.__write_dummy_file()
            return service

    def retrieve_service(self, service_id: dict):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                return existing_service
        return None

    def update_service(self, service: dict):
        pass
        # for i in list(range(0, len(self.storage))):
        #     existing_service = self.storage[i]
        #     if existing_service.get('id') == service.get('id'):
        #         self.storage[i] = service
        #         self.__write_dummy_file()
        #         return service
        # return None  # Service Not found

    def delete_service(self, service_id):
        index = None
        for i in list(range(0, len(self.storage))):
            if self.storage[i].get('id') == service_id:
                index = i
                break

        if index is not None:
            deleted_service = self.storage.pop(index)
            self.__write_dummy_file()
            return deleted_service

        return None  # Service Not found

    ####################################################################################################################
    # QUEUES METHODS
    ####################################################################################################################
    def retrieve_all_service_queues(self, service_id: str):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                return existing_service.queues
        return None  # Not queues for that service

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
                        return queue
        return None

    def delete_service_queue(self, service_id: str, queue_id: str):
        for existing_services in self.storage:
            if existing_services.get('id') == service_id:
                queue = existing_services.get('queue')
                for existing_queue in queue:
                    if existing_queue.get('id') == queue_id:
                        q = queue.pop()
                        return q
        return None  # queue not found

    def __read_dummy_file(self):
        with open(self.path, 'r') as file:
            return json.load(file)

    def __write_dummy_file(self):
        with open(self.path, 'w') as file:
            return json.dump(self.storage, file, indent=2)
