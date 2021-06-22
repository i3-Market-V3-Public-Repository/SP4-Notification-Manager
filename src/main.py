import os
from glob import glob

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from loguru import logger
from uptime import uptime

# El servicio puede ser configurado por Docker (environment vars) o por un fichero .env
load_dotenv()

# Configuración general
ENVIRONMENT_MODE = os.getenv('ENVIRONMENT_MODE', 'production')
VERSION = os.getenv('VERSION', 'undefined')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'SUPER-SECRET')
FLASK_PORT = os.getenv('FLASK_PORT', 5000)

# Flask application
application = Flask(__name__)
cors = CORS(application, resources={r"*": {"origins": "*"}})
# Flask configuration
application.config['ENV'] = ENVIRONMENT_MODE
application.config['SECRET_KEY'] = FLASK_SECRET_KEY
application.config['JSON_SORT_KEYS'] = False
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


# TODO: de momento tiramos de main y más delante si lo necesitamos lo sacamos a un fichero
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


# TODO: Notificaciones
# ServiceTask = {
#   receiver_id: string = '',
#   message: {}
# }
@application.route('/notification/service', methods=['POST'])
def notification_service():
    """
    Expect a ServiceTask in json format on the body
    :return:
    """
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    data = request.json

    return jsonify(data), 200


# NotificationTask = {
#   receiver_id: string = '',
#   _type: string = '',
#   sub_type: string = '',
#   predefined: boolean = True,
#   message: string = '' <------- ¿no es un objeto como el ServiceTask?
# }
@application.route('/notification/user', methods=['POST'])
def notification_user():
    """
    Expect a NotificationTask in json format on the body
    :return:
    """
    if not request.json:
        return jsonify({'error': 'Empty body'}), 400

    data = request.json

    return jsonify(data), 200


if __name__ == "__main__":
    logger.debug('Starting application...')
    application.run('0.0.0.0', FLASK_PORT)
