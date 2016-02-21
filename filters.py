import logging
from logmiddleware import local, NO_REQUEST_ID


class CustomLogFilter(logging.Filter):

    def filter(self, record):
        record.custom_log = getattr(local, 'custom_log', NO_REQUEST_ID)
        return True