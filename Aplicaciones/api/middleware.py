from django.http import JsonResponse
import traceback

class APIExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # manejar errores 500
        if request.path.startswith('/tasks/') or request.path.startswith('/api/'):
            return JsonResponse(
                {'error': 'Error interno del servidor', 'details': str(exception)},
                status=500
            )
        return None