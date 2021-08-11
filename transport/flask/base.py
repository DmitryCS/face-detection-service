from http import HTTPStatus
from typing import Iterable

from flask import Request, request
from flask import Response, json

from configs.config import ApplicationConfig
from context import Context


class FlaskEndpoint:

    def __call__(self, *args, **kwargs) -> Response:
        return self.handler(*args, **kwargs)

    def __init__(
            self,
            config: ApplicationConfig,
            context: Context,
            uri: str,
            methods: Iterable,
            auth_required: bool = False,
            *args, **kwargs):
        self.config = config
        self.uri = uri
        self.methods = methods
        self.context = context
        self.auth_required = auth_required
        self.__name__ = self.__class__.__name__

    @staticmethod
    def make_response_json(
            body: dict = None, status: int = 200, message: str = None, error_code: int = None
    ) -> Response:

        if body is None:
            body = {
                'message': message or HTTPStatus(status).phrase,
                'error_code': error_code or status,
            }

        return Response(response=json.dumps(body),status=status, mimetype='application/json')

    @staticmethod
    def import_body_json(request: Request) -> dict:
        if request.content_type is not None and 'application/json' in request.content_type and request.json is not None:
            return dict(request.json)
        return {}

    @staticmethod
    def import_body_headers(request: Request) -> dict:
        return {
            header: value
            for header, value in request.headers.items()
            if header.lower().startswith('x-')
        }

    def handler(self, *args, **kwargs) -> Response:
        body = {}

        body.update(self.import_body_json(request))
        body.update(self.import_body_headers(request))

        return self._method(request, body, *args, **kwargs)

    def _method(self, request: Request, body: dict, *args, **kwargs) -> Response:
        method = request.method.lower()
        func_name = f'method_{method}'  # method_get

        if hasattr(self, func_name):
            func = getattr(self, func_name)
            return func(request, body, *args, **kwargs)
        return self.method_not_impl(method=method)

    def method_not_impl(self, method: str) -> Response:
        return self.make_response_json(status=500, message=f'Method {method.upper()} not implemented')

    def method_get(self, request: Request, body: dict, *args, **kwargs) -> Response:
        return self.method_not_impl(method='GET')

    def method_post(self, request: Request, body: dict, *args, **kwargs) -> Response:
        return self.method_not_impl(method='POST')

    def method_patch(self, request: Request, body: dict, *args, **kwargs) -> Response:
        return self.method_not_impl(method='PATCH')

    def method_delete(self, request: Request, body: dict, *args, **kwargs) -> Response:
        return self.method_not_impl(method='DELETE')
