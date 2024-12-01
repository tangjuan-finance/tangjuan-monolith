from cryptography.fernet import Fernet
from flask import current_app


def encrypt_data(data: dict) -> str:
    """Encrypts dictionary data into a token."""
    import json

    KEY = current_app.config["REGISTRATION_KEY"]
    fernet = Fernet(KEY)
    return fernet.encrypt(json.dumps(data).encode()).decode()


def decrypt_data(token: str) -> dict:
    """Decrypts a token back into dictionary data."""
    import json

    KEY = current_app.config["REGISTRATION_KEY"]
    TOKEN_TTL = current_app.config["TOKEN_TTL"]

    fernet = Fernet(KEY)
    return json.loads(fernet.decrypt(token.encode(), ttl=TOKEN_TTL).decode())
