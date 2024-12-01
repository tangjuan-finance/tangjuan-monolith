from app.api.errors import ValidationError, AuthenticationError
from app.models import User
from app import db
import sqlalchemy as sa
from cryptography.fernet import InvalidToken
from app.api.utils.encryption import decrypt_data
import re
from app import create_app


def validate_username(username: str):
    """Check if username already exists."""
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is not None:
        raise ValidationError(errors={"username": "Username already taken"})


def validate_email(email: str):
    """Check if email format incorrect and already exists."""
    # Step 1: Validate email format
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        raise ValidationError(errors={"email": "Invalid email format."})

    # Step 2: Check if email already exists.
    # user = db.session.scalar(sa.select(User).where(User.email == email))

    # if user is not None:
    #     raise ValidationError(errors={"email": "Email address already registered"})

    try:
        user = db.session.scalar(sa.select(User).where(User.email == email))
        if not user:
            raise ValidationError(message="User not found")

        # Continue with processing...

    except Exception as e:
        create_app.logger.error(f"Error during registration: {e}")
        raise


def validate_token(token: str):
    """Check if email already exists."""
    try:
        data = decrypt_data(token)
        return data
    except InvalidToken:
        raise AuthenticationError(message="Invalid or expired token")
