class Subscription:
    """
    Class defining a subscription of a user (owner) with a query and or data category of the semantic engine.
    """
    def __init__(self, _id, owner, query=None, category=None):
        self.id = _id
        self.owner = owner
        if query:
            self.query = query
        if category:
            self.category = category
        self.active = True

    def to_json(self):
        json_out = {"id": self.id, "owner": self.owner}
        if hasattr(self, 'query'):
            json_out = {**json_out, **self.query}
        if hasattr(self, 'category'):
            json_out = {**json_out, **self.category}
        return json_out
