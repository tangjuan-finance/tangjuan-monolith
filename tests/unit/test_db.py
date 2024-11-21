import pytest
from app import create_app, db
from app.models import User
from config import Config
import sqlalchemy as sa


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture(scope="module", autouse=True)
def init_db():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()


def create_user(username, email, password, about_me):
    u = User(username=username, email=email, about_me=about_me)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture(scope="module")
def new_user():
    user = create_user(
        username="john",
        email="john@example.com",
        password="cat",
        about_me="about me is a long story. Just keep it cool.",
    )
    yield user


class TestUserModelCase:
    def test_create_user(self):
        # Arrange
        username = "alice"
        email = "alice@example.com"
        password = "bird"
        about_me = "Alice likes cute bird."

        user = create_user(
            username=username, email=email, password=password, about_me=about_me
        )

        # Act
        user_from_db = db.session.scalar(
            sa.select(User).where(User.username == user.username)
        )

        # Assert
        assert user_from_db.username == user.username
        assert user_from_db.email == user.email
        assert user_from_db.about_me == user.about_me
        assert user_from_db.check_password(password)

    def test_password_hashing(self):
        u = User(username="susan", email="susan@example.com")
        u.set_password("cat")
        assert not u.check_password("dog")
        assert u.check_password("cat")

    def test_create_user_in_CJK(self):
        # Arrange
        username = "使用者"
        email = "user@example.com"
        password = "cat"
        about_me = "關於使用者的一切都是秘密"

        user = create_user(
            username=username, email=email, password=password, about_me=about_me
        )

        # Act
        user_from_db = db.session.scalar(
            sa.select(User).where(User.username == user.username)
        )

        # Assert
        assert user_from_db.username == username
        assert user_from_db.about_me == about_me

    def test_avatar(self, new_user):
        assert new_user.avatar(128) == (
            "https://www.gravatar.com/avatar/"
            "d4c74594d841139328695756648b6bd6"
            "?d=identicon&s=128"
        )


class TestModelCase:
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
