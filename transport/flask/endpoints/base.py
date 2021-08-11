from transport.flask.exceptions import FlaskException
from flask import Request
from flask import Response

from transport.flask.base import FlaskEndpoint


class BaseEndpoint(FlaskEndpoint):

    def _method(self, request: Request, body: dict, *args, **kwargs) -> Response:

        database = self.context.database
        session = database.make_session()

        try:
            return super()._method(request, body, session, *args, **kwargs)

        except FlaskException as e:
            return self.make_response_json(status=e.status_code, message=str(e))
