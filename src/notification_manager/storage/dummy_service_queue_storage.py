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
                return existing_service.get('queues')
        return None  # Not queues for that service

    def retrieve_service_queue(self, service_id: str, queue_id: str):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                for queue in existing_service.get('queues'):
                    if queue.get('id') == queue_id:
                        return queue
        return None  # queue Not found

    def insert_service_queue(self, service_id: str, queue: dict):
        for existing_service in self.storage:
            if existing_service.get('id') == service_id:
                found = False
                for q in existing_service.get('queues'):
                    if q.get('name') == queue.get('name'):
                        found = True
                if not found:
                    existing_service['queues'].append(queue)
                    self.__write_dummy_file()
                    return queue
        return None

    def update_service_queue(self, service_id: str, queue: dict):
        for existing_services in self.storage:
            if existing_services.get('id') == service_id:

                for i in list(range(0, len(existing_services.get('queues')))):
                    q = existing_services['queues'][i]
                    if q.get('id') == queue.get('id'):
                        existing_services['queues'][i] = queue
                        self.__write_dummy_file()
                        return queue

        return None  # queue not found

    def delete_service_queue(self, service_id: str, queue_id: str):
        for existing_services in self.storage:
            if existing_services.get('id') == service_id:

                index = None
                for i in list(range(0, len(existing_services.get('queues')))):
                    queue = existing_services.get('queues')[i]
                    if queue.get('id') == queue_id:
                        index = i
                        break

                if index is not None:
                    queue = existing_services['queues'].pop(index)
                    self.__write_dummy_file()
                    return queue

        return None  # queue not found

    def search_services_by_queue(self, queue_name: str):
        found = {}

        for service in self.storage:
            for queue in service.get('queues'):
                if queue.get('name') == queue_name:
                    found[service.get('name')] = queue.get('endpoint') or service.get('endpoint')

        return found

    def __read_dummy_file(self):
        with open(self.path, 'r') as file:
            return json.load(file)

    def __write_dummy_file(self):
        with open(self.path, 'w') as file:
            return json.dump(self.storage, file, indent=2)
