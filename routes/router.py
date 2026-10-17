import json
import re
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.urls import path


class Router:
    """
    Router dengan gaya route Hono di atas URL Django:

        admin = Router('/admin')
        admin.get('/user/:id', auth_middleware, admin_only, user_controller.get_detail)

    Handler terakhir adalah controller `def method(self, request, **params)`,
    sisanya middleware `def middleware(request, next)`.
    Controller cukup `return { ... }` atau `return { ... }, status`.
    """

    def __init__(self, prefix=''):
        self.prefix = prefix.strip('/')
        self.routes = {}

    def get(self, rule, *handlers):
        self._add('GET', rule, handlers)

    def post(self, rule, *handlers):
        self._add('POST', rule, handlers)

    def put(self, rule, *handlers):
        self._add('PUT', rule, handlers)

    def patch(self, rule, *handlers):
        self._add('PATCH', rule, handlers)

    def delete(self, rule, *handlers):
        self._add('DELETE', rule, handlers)

    def _add(self, method, rule, handlers):
        self.routes.setdefault(rule, {})[method] = handlers

    @property
    def urls(self):
        patterns = []

        for rule, methods in self.routes.items():
            route = '/'.join(part for part in [self.prefix, rule.strip('/')] if part)
            route = re.sub(r':(\w+)', r'<\1>', route)
            patterns.append(path(route, self._view(methods)))

        return patterns

    def _view(self, methods):
        def view(request, **params):
            handlers = methods.get(request.method)

            if not handlers:
                return to_response(({ 'status': 405, 'message': 'The method is not allowed for the requested URL.', 'data': None }, 405))

            request.json = parse_body(request)
            *middlewares, controller = handlers

            def dispatch(index):
                if index == len(middlewares):
                    return to_response(controller(request, **params))
                return to_response(middlewares[index](request, lambda: dispatch(index + 1)))

            return dispatch(0)

        return view


def parse_body(request):
    if request.content_type == 'application/json':
        try:
            body = json.loads(request.body or b'{}')
            return body if isinstance(body, dict) else {}
        except ValueError:
            return {}

    return request.POST.dict()


def to_response(result):
    if isinstance(result, HttpResponse):
        return result

    body, status = result if isinstance(result, tuple) else (result, 200)

    return JsonResponse(body, status=status, encoder=DjangoJSONEncoder, safe=False)
