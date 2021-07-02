from typing import List


class Queue:
    """
    Class defining a Queue of service with a list of endpoints to send notifications.
    """
    def __init__(self, _id: str, name: str, endpoint: List[str] = None, active: bool = None):
        self.id = _id
        self.name = name
        self.endpoint = endpoint
        self.active = active

    def to_json(self):
        json_out = {"id": self.id, "name": self.name, "endpoint": self.endpoint, "active": self.active}
        return json_out


def queue_to_object(data: dict):
    return Queue(data.get('id'),
                 data.get('name'),
                 data.get('endpoint'))
