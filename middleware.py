import logging
import uuid
from django.conf import settings
from logmiddleware import local, REQUEST_ID_HEADER_SETTING, LOG_REQUESTS_SETTING, NO_REQUEST_ID, \
    REQUEST_ID_RESPONSE_HEADER_SETTING



logger = logging.getLogger(__name__)


class CustomLogMiddleware(object):
    def process_request(self, request):
        if 'operator' in request.session._session:
            agency_id = str(request.session._session['operator'].agency_id)
            username = str(request.session._session['operator'].user.username)
            custom_log = "[agency:" + agency_id + "]" + "[user:" + username + "]"
        else:
            custom_log = "[agency:None][user:None]"

        #request_id = self._get_request_id(request)
        local.custom_log = custom_log
        request.id = custom_log


    def process_response(self, request, response):
        if getattr(settings, REQUEST_ID_RESPONSE_HEADER_SETTING, False) and getattr(request, 'id', None):
            response[getattr(settings, REQUEST_ID_RESPONSE_HEADER_SETTING)] = request.id

        if not getattr(settings, LOG_REQUESTS_SETTING, False):
            return response

        # Don't log favicon
        if 'favicon' in request.path:
            return response

        user = getattr(request, 'user', None)
        user_id = getattr(user, 'pk', None) or getattr(user, 'id', None)

        message = 'method=%s path=%s status=%s'
        args = (request.method, request.path, response.status_code)

        if user_id:
            message += ' user=%s'
            args += (user_id,)

        # logger.info(message, *args)

        return response

    def _get_request_id(self, request):
        request_id_header = getattr(settings, REQUEST_ID_HEADER_SETTING, None)
        if request_id_header:
            return request.META.get(request_id_header, NO_REQUEST_ID)
        return self._generate_id()

    def _generate_id(self):
        return uuid.uuid4().hex
