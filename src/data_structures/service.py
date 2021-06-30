from typing import List

from src.data_structures.queue import Queue


class Service:
    """
    Class defining a service with its queue.
    """

    def __init__(self, _id: str, endpoint: str, queues: List[Queue] = None):
        self.id = _id
        self.endpoint = endpoint
        self.queue = queues or []

    def to_json(self):
        json_out = {"id": self.id, "endpoint": self.endpoint, "queues": map(Queue.to_json, self.queue)}
        return json_out
