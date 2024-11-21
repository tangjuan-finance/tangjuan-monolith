import pytest
from app import create_app, db
from app.models import User, Age, Salary
from tests.conftest import TestConfig


@pytest.fixture(scope="function", autouse=True)
def init_db():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()


def create_user(
    username="alice",
    email="alice@example.com",
    password="bird",
    about_me="Alice likes cute bird.",
):
    u = User(username=username, email=email, about_me=about_me)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return u


def create_age(year):
    age = Age(year=year)
    db.session.add(age)
    db.session.commit()
    return age


def create_salary(owner, start_year, name, amount=50000):
    salary = Salary(owner=owner, start_year=start_year, name=name, amount=amount)
    db.session.add(salary)
    db.session.commit()
    return salary
