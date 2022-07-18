import os

from dotenv import load_dotenv
from flask import jsonify, redirect
from flask_cors import CORS

from apiflask import APIFlask

from loguru import logger
from uptime import uptime

from src.alert_subscription.api.subscriptions_api import blueprint as subscriptions_api
from src.alert_subscription.api.subscriptions_api import config as subscriptions_config

from src.notification_manager.api.service_queue_api import blueprint as service_queue_api
from src.notification_manager.api.service_queue_api import config as service_queue_config

from src.notification_manager.api.notifications_api import blueprint as notifications_api
from src.notification_manager.api.notifications_api import config as notifications_config

from src.alert_subscription.controller.subscriptions_controller import SubscriptionsController
from src.alert_subscription.storage.dummy_subscriptions_storage import DummySubscriptionsStorage
from src.notification_manager.controller.notifications_controller import NotificationsController
from src.notification_manager.controller.service_queue_controller import QueueController
from src.notification_manager.storage.dummy_notifications_storage import DummyNotificationsStorage
from src.notification_manager.storage.dummy_service_queue_storage import DummyServiceQueueStorage
from src.utils.network import get_ip

# El servicio puede ser configurado por Docker (environment vars) o por un fichero .env
load_dotenv()


# Configuracion general
ENVIRONMENT_MODE = os.getenv('ENVIRONMENT_MODE', 'production')
VERSION = os.getenv('VERSION', 'v2.1.0')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'SUPER-SECRET')
FLASK_PORT = os.getenv('FLASK_PORT', 5000)
WEB_UI = os.getenv('WEB_UI', 'http://localhost:3000')

# Flask application
# application = Flask(__name__)
application = APIFlask(__name__,
                       docs_path='/swagger/',
                       title='Notification Manager',
                       version=VERSION
                       )

cors = CORS(application, resources={r"*": {"origins": "*"}})
# Flask configuration
application.config['ENV'] = ENVIRONMENT_MODE
application.config['SECRET_KEY'] = FLASK_SECRET_KEY
application.config['JSON_SORT_KEYS'] = False
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
application.config['OPENAPI_VERSION'] = '3.0.0'
application.config['SERVERS'] = [
    {
        'description': 'Production Server Node 1',
        'url': os.getenv("NM_NODE1", 'localhost:10010')
    },
    {
        'description': 'Production Server Node 2',
        'url': os.getenv("NM_NODE2", 'localhost:10010')
    },
    {
        'description': 'Production Server Node 3',
        'url': os.getenv("NM_NODE3", 'localhost:10010')
    },
    {
        'description': 'Development Server',
        'url': f'http://localhost:' + str(FLASK_PORT)
    }
]

application.config['INFO'] = {
    'description': 'i3-Market Notification Manager',
    # 'termsOfService': 'http://example.com',
    'contact': {
        'name': 'HOPU NM API Support',
        # 'url': 'http://www.example.com/support',
        'email': 'eleazar@hopu.org'
    },
    'license': {
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
    }
}
logger.info(f"Notification Manager Version:{VERSION}")
logger.info("Working Directory: {}".format(os.getcwd()))

### static specific ###
# SWAGGER_URL = '/swagger'
# API_URL = '/static/OLD_swagger.json'
# SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "Notification Manager API"
#     }
# )
# application.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end static specific ###


# Databases
base_storage_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
subscriptions_storage_filepath = os.path.join(base_storage_filepath, 'subscriptions_json_storage.json')
queue_storage_filepath = os.path.join(base_storage_filepath, 'queue_json_storage.json')
notifications_storage_filepath = os.path.join(base_storage_filepath, "notifications_storage.json")

subscriptions_storage = DummySubscriptionsStorage(subscriptions_storage_filepath)
queue_storage = DummyServiceQueueStorage(queue_storage_filepath)
notifications_storage = DummyNotificationsStorage(notifications_storage_filepath)

# Configuration APIs
subs_controller = SubscriptionsController(subscriptions_storage, WEB_UI)
subscriptions_config(subs_controller)
service_queue_config(QueueController(queue_storage))
notifications_config(NotificationsController(notifications_storage, WEB_UI), QueueController(queue_storage),
                     subs_controller)


# API FLASK
# @application.errorhandler(400)
# def bad_request(error):
# original_error = error.description

# if isinstance(original_error, ValidationError):
#     # custom handling
#     logger.error(f'ERROR: {original_error.message}')
#     return jsonify({'error': original_error.message}), 400

#    logger.error(f'ERROR: {error.description}')
#    return jsonify({'error': error.description}), 400


@application.route('/', methods=['GET'])
@application.doc(hide=True)
def go_to_swagger():
    return redirect('./swagger')


# TODO: Version and Health not working properly, it returns the server info, not app info
@application.route('/api/v1/version', methods=['GET'])
@application.route('/api/v1/health', methods=['GET'])
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


# Blueprints
application.register_blueprint(subscriptions_api)
application.register_blueprint(service_queue_api)
application.register_blueprint(notifications_api)

if __name__ == "__main__":
    logger.debug('Starting application...')
    logger.info("Blueprints: {}".format(application.blueprints.items()))
    application.run('0.0.0.0', FLASK_PORT)
