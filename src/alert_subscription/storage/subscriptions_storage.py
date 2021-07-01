import abc


class SubscriptionsStorage(abc.ABC):

    @abc.abstractmethod
    def retrieve_all(self):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def search_user_subscription(self, *args, **kwargs):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def insert_user_subscription(self, *args, **kwargs):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def retrieve_all_user_subscriptions(self, *args, **kwargs):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def retrieve_user_subscription(self, *args, **kwargs):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def update_user_subscription(self, *args, **kwargs):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def delete_user_subscription(self, *args, **kwargs):
        raise NotImplementedError('implement me, please!')

