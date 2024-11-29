import pytest
from app import db
from app.models import User
from flask import url_for
from app.api.utils.encryption import encrypt_data, decrypt_data
import sqlalchemy as sa


@pytest.mark.usefixtures("client")
class TestAuthRegistrationApiCase:
    def test_create_registration_vaild(self, client):
        # Arrange: Test valid email input
        valid_email = "testuser@example.com"
        # Act: Make a POST request with valid email
        response = client.post(
            url_for("api_v1.create_registration"), json={"email": valid_email}
        )

        # Assert: Check if the response status code is 200 (OK)
        assert response.status_code == 200
        assert response.json["message"] == "Registration email sent"

    def test_create_registration_invaild_duplicate_email(self, client):
        username = "alice"
        email = "alice@example.com"
        password = "bird"
        about_me = "Alice likes cute bird."

        u = User(username=username, email=email, about_me=about_me)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()

        # Arrange: Test valid email input
        duplicate_email = "alice@example.com"
        # Act: Make a POST request with valid email

        response = client.post(
            url_for("api_v1.create_registration"), json={"email": duplicate_email}
        )

        # Assert: Check if the response status code is 200 (OK)
        assert response.status_code == 400
        assert response.json["message"] == "Validation error occurred"
        assert response.json["errors"]["email"] == "Email address already registered"

    def test_create_registration_invaild_lose_email(self, client):
        # Arrange: Test valid email input
        empty_email = ""
        # Act: Make a POST request with valid email
        response = client.post(
            url_for("api_v1.create_registration"), json={"email": empty_email}
        )

        # Assert: Check if the response status code is 400 (BAD REQUEST)
        assert response.status_code == 400
        assert response.json["errors"]["email"] == "Email is required."

    def test_complete_registration(self, client, monkeypatch):
        # Arrange: Mock storage for session tokens
        mock_session_storage = {}

        def mock_save_session_token(session_token):
            """Mock implementation of save_session_token."""
            session_id = "a44932d3-d1fd-4e42-9e8e-15e8e1f7a00e"  # Fixed ID for testing
            mock_session_storage[session_id] = session_token
            return session_id

        def mock_get_session_token(session_id):
            """Mock implementation of get_session_token."""
            return mock_session_storage.get(session_id)

        # Arrange: Set up test data
        username = "Jack"
        email = "jack@example.com"
        password = "dog"
        token = encrypt_data({"email": email})
        register_url = url_for(
            "api_v1.complete_registration", token=token, _external=True
        )

        # Apply monkeypatches
        monkeypatch.setattr("app.api.auth.save_session_token", mock_save_session_token)

        # Act: Send a POST request to complete registration
        response = client.post(
            register_url, json={"username": username, "password": password}
        )

        # Assert: Check response status and message
        assert response.status_code == 200
        assert response.json["message"] == "Registration successful"

        # Assert: Check session_id
        session_id = response.json["payload"]["session_id"]
        assert session_id == "a44932d3-d1fd-4e42-9e8e-15e8e1f7a00e"

        # Assert: Verify session token
        session_token = mock_get_session_token(session_id)
        assert session_token is not None
        assert decrypt_data(session_token) == {
            "userid": User.query.filter_by(username=username).first().id
        }

        # Assert: Confirm user creation in database
        user = sa.select(User).where(User.username == username)
        assert db.session.scalar(user) is not None
