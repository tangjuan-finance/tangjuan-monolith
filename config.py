import os
from dotenv import load_dotenv
from redis import Redis

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "").replace(
        "postgres://", "postgresql://"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SESSION_TYPE = "redis"
    SESSION_REDIS = os.environ.get("SESSION_REDIS_URL") or Redis(
        host="localhost", port=6379
    )
    SESSION_PERMANENT = False
