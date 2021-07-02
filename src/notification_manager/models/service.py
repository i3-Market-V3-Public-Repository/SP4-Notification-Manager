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
        self.queues = queues or []

    def to_json(self):
        queue = map(Queue.to_json, self.queues) if self.queues else []
        json_out = {"id": self.id, "name": self.name, "endpoint": self.endpoint, "queues": queue}
        return json_out


def service_to_object(data: dict):
    return Service(data.get('id'),
                   data.get('name'),
                   data.get('endpoint'),
                   data.get('queues'))
