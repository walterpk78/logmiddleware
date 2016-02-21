from requests import Session as BaseSession
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from logmiddleware import local, REQUEST_ID_HEADER_SETTING, NO_REQUEST_ID


class Session(BaseSession):
    def __init__(self, *args, **kwargs):
        if hasattr(settings, REQUEST_ID_HEADER_SETTING):
            self.request_id_header = getattr(settings,
                                             REQUEST_ID_HEADER_SETTING)
        else:
            raise ImproperlyConfigured("The %s setting must be configured in "
                                       "order to use %s" % (
                                           REQUEST_ID_HEADER_SETTING, __name__
                                       ))
        super(Session, self).__init__(*args, **kwargs)

    def prepare_request(self, request):
        """Include the request ID, if available, in the outgoing request"""
        try:
            custom_log = local.custom_log
        except AttributeError:
            custom_log = NO_REQUEST_ID

        if self.request_id_header and custom_log != NO_REQUEST_ID:
            request.headers[self.request_id_header] = custom_log

        return super(Session, self).prepare_request(request)
