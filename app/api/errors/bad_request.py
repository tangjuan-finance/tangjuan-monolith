from app.api.errors.base import BaseCustomHTTPException

class ValidationError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Validation error occurred"
    code = 400

class EmailNotFoundError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Email is required."
    code = 400

class EmailDuplicationError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Email address already registered."
    code = 400

class EmailFormatError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Invalid email format."
    code = 400

class UserNotFoundError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "User is not founded."
    code = 400

class UserNameDuplicationError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Username already taken."
    code = 400

class UserNameFormatError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Invalid username format."
    code = 400

class UserNameNotFoundError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Username is required."
    code = 400

class PasswordNotFoundError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Password is required."
    code = 400

class PasswordInvalidError(BaseCustomHTTPException):
    """Raised when a validation error occurs."""

    description = "Password is incorrect."
    code = 400