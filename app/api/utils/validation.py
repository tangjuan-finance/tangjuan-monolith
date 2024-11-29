from app.api.errors import ValidationError, AuthenticationError
from app.models import User
from app import db
import sqlalchemy as sa
from cryptography.fernet import InvalidToken
from app.api.utils.encryption import decrypt_data


def validate_username(username: str):
    """Check if username already exists."""
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is not None:
        raise ValidationError(errors={"username": "Username already taken"})


def validate_email(email: str):
    """Check if email already exists."""
    user = db.session.scalar(sa.select(User).where(User.email == email))
    if user is not None:
        raise ValidationError(errors={"email": "Email address already registered"})


def validate_token(token: str):
    """Check if email already exists."""
    try:
        data = decrypt_data(token)
        return data
    except InvalidToken:
        raise AuthenticationError(message="Invalid or expired token")
