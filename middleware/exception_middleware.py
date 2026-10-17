import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class ExceptionMiddleware:
    """Semua error (404 route, 500, dst) dikembalikan dengan format { status, message, data }."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404 and not response.get('Content-Type', '').startswith('application/json'):
            return JsonResponse({
                'status'  : 404,
                'message' : f"Cannot {request.method} {request.path}",
                'data'    : None
            }, status=404)

        return response

    def process_exception(self, request, exception):
        logger.exception(exception)

        return JsonResponse({
            'status'  : 500,
            'message' : str(exception) or 'Internal server error',
            'data'    : None
        }, status=500)
