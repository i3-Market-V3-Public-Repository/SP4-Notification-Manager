class Queue:
    """
    Class defining a subscription of a user (owner) with a query and or data category of the semantic engine.
    """
    def __init__(self, _id: str, name: str):
        self.id = _id
        self.name = name
        self.active = True

    def to_json(self):
        json_out = {"id": self.id, "name": self.name, "active": self.active}
        return json_out
