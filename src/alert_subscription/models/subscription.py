class Subscription:
    """
    Class defining a subscription of a user (owner) with a query and or data category of the semantic engine.
    """
    def __init__(self, _id: str, category: str):
        self.id = _id
        self.category = category
        self.active = True

    def to_json(self):
        json_out = {"id": self.id, "category": self.category, "active": self.active}
        return json_out
