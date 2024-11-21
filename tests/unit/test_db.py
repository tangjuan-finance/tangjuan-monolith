import pytest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture(scope="module")
def init_db(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    self.app_context.pop()


class TestUserModelCase:
    def test_password_hashing(self):
        u = User(username="susan", email="susan@example.com")
        u.set_password("cat")
        assert not u.check_password("dog")
        assert u.check_password("cat")

    def test_avatar(self):
        u = User(username="john", email="john@example.com")
        assert u.avatar(128) == (
            "https://www.gravatar.com/avatar/"
            "d4c74594d841139328695756648b6bd6"
            "?d=identicon&s=128"
        )
