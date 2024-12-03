from app.api.errors.base import BaseCustomHTTPException


class AuthenticationError(BaseCustomHTTPException):
    """Raised when authentication fails."""

    description = "Authentication error occurred"
    code = 401


class InvalidRegistrationTokenError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Invalid or expired registration token"
    code = 401


class InvalidAuthenticationTokenError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Invalid or expired authentication token"
    code = 401
