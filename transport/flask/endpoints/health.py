from flask import Request
from flask import Response

from transport.flask.base import FlaskEndpoint


class HealthEndpoint(FlaskEndpoint):

    def method_get(self, request: Request, body: dict,  *args, **kwargs) -> Response:
        response = {
            'hello': 'world'
        }
        return self.make_response_json(body=response, status=200)
