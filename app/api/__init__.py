from flask import Blueprint

bp = Blueprint("api_v1", __name__)

from app.api import auth  # noqa: E402, F401
from app.api.errors import handler  # noqa: E402, F401
