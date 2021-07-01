from typing import List

from src.notification_manager.models.queue import Queue


class Service:
    """
    Class defining a service with its queue.
    """

    def __init__(self, _id: str, name: str, endpoint: List[str] = None, queues: List[Queue] = None):
        self.id = _id
        self.name = name
        self.endpoint = endpoint
        self.queue = queues or []

    def to_json(self):
        json_out = {"id": self.id, "endpoint": self.endpoint, "queues": map(Queue.to_json, self.queue)}
        return json_out


def service_to_object(data: dict):
    return Service(data.get('id'),
                   data.get('endpoint'),
                   data.get('queue'))
