import abc


class NotificationsStorage(abc.ABC):

    @abc.abstractmethod
    def retrieve_all(self):
        raise NotImplementedError('implement me, please!')

    def retrieve_all_unread(self):
        raise NotImplementedError('implement me, please!')

    ####################################################################################################################
    # NOTIFICATIONS METHODS
    ####################################################################################################################
    @abc.abstractmethod
    def insert_notification(self, notification: dict):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def read_notification(self, notification_id, read: bool):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def retrieve_notification(self, notification_id: str):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def retrieve_notification_by_user(self, user_id: str):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def retrieve_unread_notification_by_user(self, user_id: str):
        raise NotImplementedError('implement me, please!')

    @abc.abstractmethod
    def delete_notification(self, notification_id: str):
        raise NotImplementedError('implement me, please!')


