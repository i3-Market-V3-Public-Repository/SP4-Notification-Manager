import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from loguru import logger
from uptime import uptime

from src.alert_subscription.api.subscriptions_api import api as subscriptions_api
from src.alert_subscription.api.subscriptions_api import config as subscriptions_config

from src.notification_manager.api.service_queue_api import api as service_queue_api
from src.notification_manager.api.service_queue_api import config as service_queue_config

from src.notification_manager.api.notifications_api import api as notifications_api
from src.notification_manager.api.notifications_api import config as notifications_config

# El servicio puede ser configurado por Docker (environment vars) o por un fichero .env
from src.alert_subscription.controller.subscriptions_controller import SubscriptionsController
from src.alert_subscription.storage.dummy_subscriptions_storage import DummySubscriptionsStorage
from src.notification_manager.controller.notifications_controller import NotificationsController
from src.notification_manager.controller.service_queue_controller import QueueController
from src.notification_manager.storage.dummy_service_queue_storage import DummyServiceQueueStorage

load_dotenv()

# Configuración general
ENVIRONMENT_MODE = os.getenv('ENVIRONMENT_MODE', 'production')
VERSION = os.getenv('VERSION', 'v0.2')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'SUPER-SECRET')
FLASK_PORT = os.getenv('FLASK_PORT', 5000)
WEB_UI = os.getenv('WEB_UI', 'http://localhost:3000')

# Flask application
application = Flask(__name__)
cors = CORS(application, resources={r"*": {"origins": "*"}})
# Flask configuration
application.config['ENV'] = ENVIRONMENT_MODE
application.config['SECRET_KEY'] = FLASK_SECRET_KEY
application.config['JSON_SORT_KEYS'] = False
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Blueprints
application.register_blueprint(subscriptions_api)
application.register_blueprint(service_queue_api)
application.register_blueprint(notifications_api)
# Databases
base_storage_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
subscriptions_storage_filepath = os.path.join(base_storage_filepath, 'subscriptions_json_storage.json')
queue_storage_filepath = os.path.join(base_storage_filepath, 'queue_json_storage.json')

subscriptions_storage = DummySubscriptionsStorage(subscriptions_storage_filepath)
queue_storage = DummyServiceQueueStorage(queue_storage_filepath)

# Configuration APIs
subs_controller = SubscriptionsController(subscriptions_storage, WEB_UI)
subscriptions_config(subs_controller)
service_queue_config(QueueController(queue_storage))
notifications_config(NotificationsController(), QueueController(queue_storage), subs_controller)


# API FLASK
@application.errorhandler(400)
def bad_request(error):
    # original_error = error.description

    # if isinstance(original_error, ValidationError):
    #     # custom handling
    #     logger.error(f'ERROR: {original_error.message}')
    #     return jsonify({'error': original_error.message}), 400

    logger.error(f'ERROR: {error.description}')
    return jsonify({'error': error.description}), 400


# TODO: SWAGGER
@application.route('/swagger', methods=['GET'])
def swagger():
    pass


# TODO: Version and Health
@application.route('/version', methods=['GET'])
@application.route('/health', methods=['GET'])
def version():
    up_time = uptime()
    hours, remainder = divmod(up_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    return jsonify(
        name='i3-market NotificationManager',
        version=VERSION,
        uptime=f'{int(days)} d, {int(hours)} h, {int(minutes)} m, {int(seconds)} s'
    ), 200


if __name__ == "__main__":
    logger.debug('Starting application...')
    application.run('0.0.0.0', FLASK_PORT)
