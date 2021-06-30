# import uuid
#
# from src.alert_subscription.models.subscription import Subscription
#
# user_topic_link = {"usuario1": ["Obj{id:1,querie:asd,active:true}"]}  # lista para enlazar usuarios a sus suscripciones
#
# stored_subs = {  # diccionario para enlazar categorias, queries y sus usuarios suscritos.
#     # Organizadas por categorias?
#     # "all": [Obj{"id": 1, "query": "iot", "owner": "user1", "active": True},
#     #         Obj{"id": 2, "query": "iot", "owner": "user2", "active": True}],
#
#     # "smartcity": [{"id": 2, "query": "iot", "owner": "user2", "active": True}],
#
#     # Organizadas por categorias y queries?
#     # "all": {"iot":["id": 1, "owner": "user1", "active": True]}
#
#     # Organizadas por queries?
#     # "iot": [{"id": 1, "category": "all", "owner": "usuario1", "active": True},
#     #        {"id": 2, "category": "smartcity", "owner": "usuario3", "active": True}]
#
#     # Organizadas por usuarios?
#     # "usuario1": ["categoryX": [{"query":""}]]
#     # "usuario2": ["categoryX": [{"query":""}]]
# }
#
#
# def __add_subscription__(new_sub: Subscription):
#     cat = new_sub.category
#     if stored_subs.get(cat):
#         # category exist in stored subs
#         for existing_sub in stored_subs[cat]:  # loop: list of subsription
#             if existing_sub.owner == new_sub.owner and existing_sub.query == new_sub.query:
#                 # already exist sub
#                 return True
#             elif existing_sub.owner == new_sub.owner and existing_sub.query != new_sub.query:
#                 # updating query?
#                 existing_sub.query = new_sub.query
#                 return True
#         stored_subs[cat].append(new_sub)
#         return True
#     else:
#         stored_subs[new_sub.category] = list().append(new_sub)
#         return True
#
#
# def create_subscription(user, query=None, category=None):
#     if not query and not category:
#         return False
#     if query and not category:
#         category = 'all'
#
#     new_id = uuid.uuid4()
#     sub = Subscription(new_id, user, query, category)
#     return __add_subscription__(sub)
#
#
# def delete_subscription(id):
#     pass
#
#
# def modify_subscription(owner, query, category, active):
#     pass
#
#
# def get_subscriptions(owner):
#     pass
