import pytest
from app import db
from app.models import User
from flask import url_for
from app.api.utils.validation import validate_token
from app.api.utils.encryption import encrypt_data, decrypt_data
from app.api.services.redis_service import get_session_token
import sqlalchemy as sa
import re


@pytest.mark.usefixtures("client")
class TestAuthRegistrationApiCase:
    def test_create_registration_vaild(self, client, monkeypatch):
        mock_save_email_sent = {}

        # Arrange: Test valid email input
        def mock_send_email(to_email, subject, content):
            mock_save_email_sent["to_email"] = to_email
            # Regular expression to match a URL
            url_pattern = r"https?://[^\s]+"
            # Search for the URL in the text
            match = re.search(url_pattern, content)
            # Extract and print the URL if found
            if match:
                mock_save_email_sent["register_url"] = match.group(0)
            else:
                mock_save_email_sent["register_url"] = ""

        valid_email = "testuser@example.com"

        # Apply monkeypatches to send_email
        monkeypatch.setattr("app.api.auth.send_email", mock_send_email)

        # Act: Make a POST request with valid email
        response = client.post(
            url_for("api_v1.create_registration"), json={"email": valid_email}
        )

        # Assert: Check if the response status code is 200 (OK)
        assert response.status_code == 200
        assert response.json["message"] == "Registration email sent"

        # Assert: Check if the email send is the same as the email provided
        assert mock_save_email_sent["to_email"] == valid_email

        # Retrieve the expected URL
        expected_url = mock_save_email_sent.get("register_url")

        # Ensure the URL is provided
        if not expected_url:
            pytest.fail(
                "The URL is not provided"
            )  # Raise an error if the URL is missing

        # Define the regular expression pattern
        pattern = r"http://[^/]+/([^/]+/[^/]+/[^/]+)/([^/]+)"

        # Match and extract parts of the URL
        match = re.search(pattern, expected_url)
        if match:
            api_path = match.group(1)  # Extract "api/v1/register"
            token = match.group(2)  # Extract "gAAAAABnSHBURM-H9f5qoH......"

            # Validate extracted parts
            assert (
                api_path == "api/v1/register"
            ), f"Expected 'api/v1/register', got '{api_path}'"
            assert token is not None, "Token extraction failed"

            assert decrypt_data(token, mode="registration") == {"email": valid_email}
        else:
            pytest.fail(
                "No match found for the URL"
            )  # Fail the test if regex doesn't match

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
        assert response.json["error"]["code"] == "EmailDuplicationError"
        assert response.json["error"]["message"] == "Email address already registered"
        assert (
            response.json["error"]["fields"]["email"]
            == "Email address already registered"
        )

    def test_create_registration_invaild_lose_email(self, client):
        # Arrange: Test valid email input
        empty_email = ""
        # Act: Make a POST request with valid email
        response = client.post(
            url_for("api_v1.create_registration"), json={"email": empty_email}
        )

        # Assert: Check if the response status code is 400 (BAD REQUEST)
        assert response.status_code == 400
        assert response.json["error"]["code"] == "EmailNotFoundError"
        assert response.json["error"]["fields"]["email"] == "Email is required"

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
        token = encrypt_data({"email": email}, mode="registration")
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
        assert decrypt_data(session_token, mode="authentication") == {
            "userid": User.query.filter_by(username=username).first().id
        }

        # Assert: Confirm user creation in database
        user = sa.select(User).where(User.username == username)
        assert db.session.scalar(user) is not None

    def test_fake_token_imcomplete_registration(self, client):
        # Arrange: Set up test data

        fake_token = "hAAAAABnSHBURM-H9f5qoHC3pRXn55aJFEC-bjzlqJM8ew-ZXVk3XslLGpqc5h7nrBuy01xeAP7cQvJves1FadtAoQuqF0PZ1soxqyk9reWEy7D5KWbW2Qs\\="
        register_url = url_for(
            "api_v1.complete_registration", token=fake_token, _external=True
        )
        username = "FakeJack"
        password = "hotdog"

        # Act: Send a POST request to complete registration
        response = client.post(
            register_url, json={"username": username, "password": password}
        )

        # Assert: Check response status and message
        assert response.status_code == 401
        assert response.json["error"]["code"] == "InvalidRegistrationTokenError"
        assert (
            response.json["error"]["message"] == "Invalid or expired registration token"
        )
        assert (
            response.json["error"]["fields"]["token"]
            == "Invalid or expired registration token"
        )

    def test_no_username_imcomplete_registration(self, client):
        # Arrange: Set up test data

        email = "textemail2@gmail.com"
        token = encrypt_data({"email": email}, mode="registration")
        # token = "gAAAAABnTY_M29aXWbyTFm35GR4GURbEjn5JYC3jhtmoa_g0gYgNs9EVJlYVsfAjfE-LKz1uVCvV801URdukQdHjOnuEFITPPL9Xpdsns2Mn2xaz4mdwtqmSDyBVRz9s-4EemY42Gd8E"
        register_url = url_for(
            "api_v1.complete_registration", token=token, _external=True
        )
        username = ""
        password = "textemail2secret"

        # Act: Send a POST request to complete registration
        response = client.post(
            register_url, json={"username": username, "password": password}
        )

        # Assert: Check response status and message
        assert response.status_code == 400
        assert response.json["error"]["code"] == "UserNameNotFoundError"
        assert response.json["error"]["message"] == "Username is required"
        assert response.json["error"]["fields"]["username"] == "Username is required"

    def test_no_password_imcomplete_registration(self, client):
        # Arrange: Set up test data

        email = "textemail2@gmail.com"
        token = encrypt_data({"email": email}, mode="registration")
        # token = "gAAAAABnTY_M29aXWbyTFm35GR4GURbEjn5JYC3jhtmoa_g0gYgNs9EVJlYVsfAjfE-LKz1uVCvV801URdukQdHjOnuEFITPPL9Xpdsns2Mn2xaz4mdwtqmSDyBVRz9s-4EemY42Gd8E"
        register_url = url_for(
            "api_v1.complete_registration", token=token, _external=True
        )
        username = "textemail2"
        password = ""

        # Act: Send a POST request to complete registration
        response = client.post(
            register_url, json={"username": username, "password": password}
        )

        # Assert: Check response status and message
        assert response.status_code == 400
        assert response.json["error"]["code"] == "PasswordNotFoundError"
        assert response.json["error"]["message"] == "Password is required"
        assert response.json["error"]["fields"]["password"] == "Password is required"

    def test_duplicate_username_imcomplete_registration(self, client):
        # Arrange: Set up test data

        email = "textemail2@gmail.com"
        token = encrypt_data({"email": email}, mode="registration")
        # token = "gAAAAABnTY_M29aXWbyTFm35GR4GURbEjn5JYC3jhtmoa_g0gYgNs9EVJlYVsfAjfE-LKz1uVCvV801URdukQdHjOnuEFITPPL9Xpdsns2Mn2xaz4mdwtqmSDyBVRz9s-4EemY42Gd8E"
        register_url = url_for(
            "api_v1.complete_registration", token=token, _external=True
        )
        username = "default"
        password = "secret"

        # Act: Send a POST request to complete registration
        response = client.post(
            register_url, json={"username": username, "password": password}
        )

        # Assert: Check response status and message
        # UserNameDuplicationError(errors={"username": "Username already taken."})
        assert response.status_code == 400
        assert response.json["error"]["code"] == "UserNameDuplicationError"
        assert response.json["error"]["message"] == "Username already taken"
        assert response.json["error"]["fields"]["username"] == "Username already taken"


@pytest.mark.usefixtures("client")
class TestAuthLoginApiCase:
    def test_complete_login(self, client):
        # Arrange: Create a user for test

        # Use default user
        email = "default@example.com"
        password = "secret"

        user = db.session.scalar(sa.select(User).where(User.email == email))

        # Act: Send a POST request to Login
        response = client.post(
            url_for("api_v1.login"), json={"email": email, "password": password}
        )

        # Assert: Check response status and message
        assert response.status_code == 200
        assert response.json["message"] == "Login successful"

        session_id = response.json["payload"]["session_id"]
        session_token = get_session_token(session_id)

        retrieve_user_id = validate_token(session_token, mode="authentication")[
            "userid"
        ]

        assert user.id == retrieve_user_id

    def test_missing_info_incomplete_login(self, client):
        # Arrange: Create a user for test

        email = "loginbro@example.com"
        password = "bro_is_c00l!"

        # Act: Send a POST request to Login
        response = client.post(
            url_for("api_v1.login"), json={"email": "", "password": password}
        )

        # Assert: Check response status and message
        # Assert: Check response status and message
        assert response.status_code == 400
        assert response.json["error"]["code"] == "EmailNotFoundError"
        assert response.json["error"]["message"] == "Email is required"
        assert response.json["error"]["fields"]["email"] == "Email is required"

        # Act: Send a POST request to Login
        response = client.post(
            url_for("api_v1.login"), json={"email": email, "password": ""}
        )

        # Assert: Check response status and message
        assert response.status_code == 400
        assert response.json["error"]["code"] == "PasswordNotFoundError"
        assert response.json["error"]["message"] == "Password is required"
        assert response.json["error"]["fields"]["password"] == "Password is required"

    def test_user_not_found_incomplete_login(self, client):
        # Arrange: Create a user for test

        email = "youcantseeme@example.com"
        password = "thereis*nothing*nothing"

        # Act: Send a POST request to Login
        response = client.post(
            url_for("api_v1.login"), json={"email": email, "password": password}
        )

        # Assert: Check response status and message
        # Assert: Check response status and message
        assert response.status_code == 400
        assert response.json["error"]["code"] == "UserNotFoundError"
        assert response.json["error"]["message"] == "User is not founded"
        assert response.json["error"]["fields"]["user"] == "User is not founded"

    def test_incorrect_pw_incomplete_login(self, client, monkeypatch):
        # Arrange: Create a user for test

        # Use default user
        email = "default@example.com"
        incorrect_password = "bad_secret"

        # Act: Send a POST request to Login
        response = client.post(
            url_for("api_v1.login"),
            json={"email": email, "password": incorrect_password},
        )

        # Assert: Check response status and message
        # Assert: Check response status and message
        assert response.status_code == 400
        assert response.json["error"]["code"] == "PasswordInvalidError"
        assert response.json["error"]["message"] == "Password is incorrect"
        assert response.json["error"]["fields"]["password"] == "Password is incorrect"
