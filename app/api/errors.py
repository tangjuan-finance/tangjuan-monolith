from werkzeug.exceptions import HTTPException
from app.api import bp
from flask import jsonify


class ValidationError(HTTPException):
    code = 400
    description = "Validation error occurred"

    def __init__(self, message=None, errors=None):
        super().__init__(description=message or self.description)
        self.errors = errors or {}

    def to_dict(self):
        return {
            "status": self.code,
            "error": self.name,
            "message": self.description,
            "errors": self.errors,
        }


class AuthenticationError(HTTPException):
    code = 400
    description = "Authentication error occurred"

    def __init__(self, message=None, errors=None):
        super().__init__(description=message or self.description)
        self.errors = errors or {}

    def to_dict(self):
        return {
            "status": self.code,
            "error": self.name,
            "message": self.description,
            "errors": self.errors,
        }


@bp.errorhandler(ValidationError)
def handle_validation_error(e):
    response = jsonify(e.to_dict())
    response.status_code = e.code
    return response


@bp.errorhandler(HTTPException)
def handle_http_exception(e):
    response = {"status": e.code, "error": e.name, "message": e.description}
    return jsonify(response), e.code


@bp.errorhandler(Exception)
def handle_generic_exception(e):
    response = {"status": 500, "error": "Internal Server Error", "message": str(e)}
    return jsonify(response), 500
