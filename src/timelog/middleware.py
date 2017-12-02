import logging
import timeit

from django.db import connection
from django.utils.encoding import smart_str

logger = logging.getLogger(__name__)


class TimeLogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        start = timeit.default_timer()

        response = self.get_response(request)

        sqltime = 0.0

        for q in connection.queries:
            sqltime += float(getattr(q, 'time', 0.0))

        if hasattr(request, '_start'):
            d = {
                'method': request.method,
                'time': timeit.default_timer() - start,
                'code': response.status_code,
                'url': smart_str(request.path_info),
                'sql': len(connection.queries),
                'sqltime': sqltime,
            }
            msg = '%(method)s "%(url)s" (%(code)s) %(time).2f (%(sql)dq, %(sqltime).4f)' % d
            logger.info(msg)
        return response
