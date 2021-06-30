class Subscription:
    """
    Class defining a subscription of a user (owner) with a query and or data category of the semantic engine.
    """
    def __init__(self, _id: str, category: str, active: bool = True):
        self.id = _id
        self.category = category
        self.active = active

    def to_json(self):
        json_out = {"id": self.id, "category": self.category, "active": self.active}
        return json_out


def subscription_to_object(data: dict):
    return Subscription(data.get('id'),
                        data.get('category'),
                        data.get('active'))
