from typing import List


class Queue:
    """
    Class defining a subscription of a user (owner) with a query and or data category of the semantic engine.
    """
    def __init__(self, _id: str, name: str, endpoint: List[str] = None):
        self.id = _id
        self.name = name
        self.endpoint = endpoint
        self.active = True

    def to_json(self):
        json_out = {"id": self.id, "name": self.name, "endpoint": self.endpoint, "active": self.active}
        return json_out
