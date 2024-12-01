import os
from dotenv import load_dotenv
from redis import Redis

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    REGISTRATION_KEY = os.environ.get("REGISTRATION_KEY")
    try:
        TOKEN_TTL = int(os.environ.get("TOKEN_TTL"))
    except ValueError:
        TOKEN_TTL = 604800
        # One Week
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "").replace(
        "postgres://", "postgresql://"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    if os.environ.get("TOKEN_REDIS_URL"):
        REDIS_CLIENT = Redis.from_url(
            os.environ.get("TOKEN_REDIS_URL"), decode_responses=True
        )
    else:
        REDIS_CLIENT = Redis(host="localhost", port=6379, decode_responses=True)
    # Add SQLAlchemy configuration for connection pooling
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True  # Enable pre-ping to check connections
    }
