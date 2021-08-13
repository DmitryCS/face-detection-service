class FlaskException(Exception):
    status_code = 500


class FlaskRequestValidationException(FlaskException):
    status_code = 400
