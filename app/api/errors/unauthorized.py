from app.api.errors.base import BaseCustomHTTPException

class AuthenticationError(BaseCustomHTTPException):
    """Raised when authentication fails."""

    description = "Authentication error occurred"
    code = 401