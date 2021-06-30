import abc


class Storage(abc.ABC):

    @abc.abstractmethod
    def create_user_subscription(self, *args, **kwargs):
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

