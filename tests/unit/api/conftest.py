import pytest
from app import create_app, db
from tests.conftest import TestConfig


@pytest.fixture(scope="module")
def client():
    # Create the app and push the app context
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()

    # Push the request context so that the url_for() could work
    test_request_context = app.test_request_context()
    test_request_context.push()

    # Initialize the database
    db.create_all()

    # Use the app's test client for the test
    with app.test_client() as client:
        yield client  # This is the test client that you can use in your tests

    # Cleanup: Remove session, drop tables, and pop app context
    db.session.remove()
    db.drop_all()
    app_context.pop()
    test_request_context.pop()
