from werkzeug.exceptions import BadRequest
from app.models import User
from app import db
import sqlalchemy as sa


def validate_username(username):
    """Check if username already exists."""
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is not None:
        raise BadRequest("Username already taken.")


def validate_email(email):
    """Check if email already exists."""
    user = db.session.scalar(sa.select(User).where(User.email == email))
    if user is not None:
        raise BadRequest("Email already registered.")
