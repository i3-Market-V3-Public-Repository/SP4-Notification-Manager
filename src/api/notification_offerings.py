from flask import Blueprint, request, jsonify
from loguru import logger

from src.storage.storage import Storage

api = Blueprint('queues', __name__)
# noinspection PyTypeChecker
__adapter: Storage = None


def config_database(adapter: Storage):
    global __adapter
    __adapter = adapter


# Expenses
@api.route('/offering/', methods=['POST'])
def post_offering():
    pass
