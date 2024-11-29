from app.api.errors import ValidationError
from app.models import User
from app import db
import sqlalchemy as sa


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
