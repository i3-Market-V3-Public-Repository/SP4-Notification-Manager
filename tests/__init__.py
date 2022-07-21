OK_CODE = 200
NOT_FOUND_CODE = 404
BODY_ERROR_CODE = 400
BASE_API = '/api/v1'
ALREADY_EXIST_BODY = {'detail': {}, 'message': 'Already exists subscription to category'}
ALREADY_EXIST_SERVICE_BODY = {'detail': {}, 'message': 'Already exists'}
NOT_FOUND_BODY = {'detail': {}, 'message': 'Not Found'}
# INCOMPLETE_BODY = {'detail': {}, 'message': 'Incomplete Body'}
QUEUE_ERROR_BODY = {'detail': {'json': {'name': ['Must be one of: offering.new, offering.update, '
                                            'agreement.accepted, agreement.rejected, '
                                            'agreement.update, agreement.pending, '
                                            'agreement.termination, agreement.claim.']}},
               'message': 'Validation error'}
