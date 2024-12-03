from cryptography.fernet import Fernet
from flask import current_app


def encrypt_data(data: dict, mode: str) -> str:
    """Encrypts dictionary data into a token."""
    import json

    if mode == "registration":
        KEY = current_app.config["REGISTRATION_KEY"]
    elif mode == "authentication":
        KEY = current_app.config["AUTHENTICATION_KEY"]
    else:
        raise ValueError(
            f"Invalid mode: {mode}. Expected 'registration' or 'authentication'."
        )
    fernet = Fernet(KEY)
    return fernet.encrypt(json.dumps(data).encode()).decode()


def decrypt_data(token: str, mode: str) -> dict:
    """Decrypts a token back into dictionary data."""
    import json

    if mode == "registration":
        KEY = current_app.config["REGISTRATION_KEY"]
    elif mode == "authentication":
        KEY = current_app.config["AUTHENTICATION_KEY"]
    else:
        raise ValueError(
            f"Invalid mode: {mode}. Expected 'registration' or 'authentication'."
        )
    TOKEN_TTL = current_app.config["TOKEN_TTL"]

    fernet = Fernet(KEY)
    return json.loads(fernet.decrypt(token.encode(), ttl=TOKEN_TTL).decode())
