from enum import Enum

from fortika_lib_rabbit import Task
from loguru import logger

from utils.rabbit.async_rabbit_publisher import AsyncRabbitMQClientManager

# TODO: (source) https://gitlab.fokus.fraunhofer.de/WP4-fortika-modules-components/marketplace-device-manager/-/blob/v0.3.6g/devices_communication_manager/devices_event_listener/executors/async/helpers/notification_sevice_client.py
# TODO: Entiendo que hay que descargarse https://gitlab.fokus.fraunhofer.de/WP4-fortika-modules-components/marketplace-device-manager/-/tree/v0.3.6g/utils/rabbit
# TODO: y el paquete de fortika_lib_rabbit


class AsyncNotificationServiceClient:
    class Type(Enum):
        SYSTEM = '0'
        ORGANIZATION = '1'
        USER_PUBLIC = '2'
        USER_PRIVATE = '3'
        DIRECT = '4'

    class Subtype(Enum):
        USER = 'user'
        BUNDLE_PUBLISHING = 'bundle_publishing'
        BUNDLE_PURCHASING = 'bundle_purchasing'
        GATEWAY_STATS = 'gateway_stats'
        BUNDLE_INSTANCES = 'bundle_instances'

    @staticmethod
    def __call_back(status):
        logger.debug("Response Status: {}".format(status))

    @staticmethod
    def __get_task(item_id, _type: Type, subtype: Subtype, message) -> Task:
        details = {
            'channel_options': {
                'item_id': item_id,
                'type': _type.value,
                'sub_type': subtype.value,
                'predefined': True,
            },
            'item': {
                'message': message
            }
        }
        return Task('notification_processor.notification.find_channel_then_create', details)

    @staticmethod
    async def send(item_id, notification_type, notification_subtype, message: str):
        task = AsyncNotificationServiceClient.__get_task(
            item_id,
            notification_type,
            notification_subtype,
            message
        )
        await AsyncRabbitMQClientManager().send_task(
            task,
            callback=AsyncNotificationServiceClient.__call_back
        )
