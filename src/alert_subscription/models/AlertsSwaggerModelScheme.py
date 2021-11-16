import apiflask.fields
from loguru import logger

from apiflask import Schema
from apiflask.fields import String, Integer, List, Dict, Boolean
from apiflask.validators import Length, OneOf


class Subscription(Schema):
    subscription_id = String(required=True, description='Autogenerated id for identification')
    category = String(required=True, description='Category the user subscribes to')
    active = Boolean(required=True, description='Describes if the subscription is active or not')


class SubscriptionList(Schema):
    subscriptions = Subscription