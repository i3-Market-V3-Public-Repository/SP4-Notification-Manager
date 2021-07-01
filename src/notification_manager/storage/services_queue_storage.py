import abc


class ServicesQueueStorage(abc.ABC):

    @abc.abstractmethod
    def retrieve_all(self):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def search_service_by_queue(self):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def create_service(self):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def insert_service_queue(self):
        raise NotImplementedError('implement me, please!')