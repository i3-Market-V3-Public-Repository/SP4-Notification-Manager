import abc


class ServicesQueueStorage(abc.ABC):

    @abc.abstractmethod
    def retrieve_all(self):
        raise NotImplementedError('implement me, please!')

    ####################################################################################################################
    # SERVICES METHODS
    ####################################################################################################################
    @abc.abstractmethod
    def insert_service(self, service: dict):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def update_service(self, service: dict):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def retrieve_service(self, service_id: str):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def delete_service(self, service_id: str):
        raise NotImplementedError('implement me, please!')

    ####################################################################################################################
    # QUEUES METHODS
    ####################################################################################################################
    @abc.abstractmethod
    def retrieve_all_service_queues(self, service_id: str):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def retrieve_service_queue(self, service_id: str, queue_id: str):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def insert_service_queue(self, service_id: str, queue: dict):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def update_service_queue(self, service_id: str, queue: dict):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def delete_service_queue(self, service_id: str, queue_id: str):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def get_service_endpoint_by_queue_name_if_active(self, queue_name: str):
        raise NotImplementedError('implement me, please!')

    def get_service_endpoint_by_market_id_if_active(self, market_id: str, queue_name: str):
        raise NotImplementedError('implement me, please!')
