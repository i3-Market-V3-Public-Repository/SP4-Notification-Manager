from src.notification_manager.models import queue_types
from src.notification_manager.models.queue_types import QueueType

OK_CODE = 200
NOT_FOUND_CODE = 404
BODY_ERROR_CODE = 400
BASE_API = '/api/v1'
ALREADY_EXIST_BODY = {'detail': {}, 'message': 'Already exists subscription to category'}
ALREADY_EXIST_SERVICE_BODY = {'detail': {}, 'message': 'Already exists'}
NOT_FOUND_BODY = {'detail': {}, 'message': 'Not Found'}
# INCOMPLETE_BODY = {'detail': {}, 'message': 'Incomplete Body'}
queues_type = ', '.join([q.value for q in QueueType.__members__.values()]) + '.'
QUEUE_ERROR_BODY = {'detail': {'json': {'name': [f"Must be one of: {queues_type}"
                                                 # 'offering.new, offering.update, '
                                                 # 'agreement.accepted, agreement.rejected, '
                                                 # 'agreement.update, agreement.pending, '
                                                 # 'agreement.termination, agreement.claim.'

                                                 ]}},
                    'message': 'Validation error'}
