import structlog
logger = structlog.get_logger('base')

class RequestResponseLogMiddleware:
    LOGGED_HEADERS = ["CONTENT_LENGTH", "CONTENT_TYPE", "HTTP_HOST", "HTTP_PROXY"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info('Request started', **self._get_request_data(request))

        response = self.get_response(request)

        logger.info('Request completed', **self._get_response_data(response, request))

        return response

    def _get_request_data(self, request):
        return {
            'get_params': {field_name: request.GET.getlist(field_name) for field_name in request.GET.keys()},
            'request_headers': {header_name: request.META[header_name] for header_name in self.LOGGED_HEADERS
                if header_name in request.META},
            'url': request.path_info,
            'method': request.method,
        }

    def _get_response_data(self, response, request):
        result = {
            'status_code': response.status_code,
            'url': request.path_info,
            'method': request.method,
        }
        return result
