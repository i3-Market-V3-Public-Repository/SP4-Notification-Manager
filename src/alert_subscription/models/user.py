from typing import List

from src.alert_subscription.models.subscription import Subscription


class User:
    """
    Class defining a user with its subscriptions.
    """
    def __init__(self, _id: str, subscriptions: List[Subscription] = None):
        self.id = _id
        self.subscriptions = subscriptions or []

    def to_json(self):
        json_out = {"id": self.id, "subscriptions": map(Subscription.to_json, self.subscriptions)}
        return json_out
