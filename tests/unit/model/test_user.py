from app import db
from app.models import User
import sqlalchemy as sa
from tests.unit.model.conftest import create_user


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

    def test_avatar(self):
        u = User(username="john", email="john@example.com")
        assert u.avatar(128) == (
            "https://www.gravatar.com/avatar/"
            "d4c74594d841139328695756648b6bd6"
            "?d=identicon&s=128"
        )


class TestUserOwnershipModelCase:
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
