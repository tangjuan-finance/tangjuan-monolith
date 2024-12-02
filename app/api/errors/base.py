from werkzeug.exceptions import HTTPException
import datetime

class BaseCustomHTTPException(HTTPException):
    """Base class for all custom HTTP exceptions."""

    description = "An error occurred"

    def __init__(self, message=None, errors=None):
        # If a message is provided, use it; otherwise, use the default description
        super().__init__(description=message or self.description)
        self.errors = errors or {}

    @property
    def name(self):
        """Use the class name as the error name."""
        return self.__class__.__name__

    def to_dict(self):
        """Convert error to dictionary for response."""
        return {
            "status": "error",
            "statusCode": self.code,
            "error": {
                "code": self.name,
                "message": self.description,
                "fields": self.errors,
                "timestamp": datetime.datetime.now(),
            },
        }