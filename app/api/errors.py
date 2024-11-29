from werkzeug.exceptions import HTTPException
from app.api import bp
from flask import jsonify


class BaseCustomHTTPException(HTTPException):
    """Base class for all custom HTTP exceptions."""

    code = 400
    description = "An error occurred"

    def __init__(self, message=None, errors=None):
        # If a message is provided, use it; otherwise, use the default description
        super().__init__(description=message or self.description)
        self.errors = errors or {}

    def to_dict(self):
        """Convert error to dictionary for response."""
        return {
            "status": self.code,
            "error": self.name,
            "message": self.description,
            "errors": self.errors,
        }


class ValidationError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Validation error occurred"
    code = 400


class AuthenticationError(BaseCustomHTTPException):
    """Raised when authentication fails."""

    description = "Authentication error occurred"
    code = 401


@bp.errorhandler(BaseCustomHTTPException)
def handle_custom_error(e):
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
