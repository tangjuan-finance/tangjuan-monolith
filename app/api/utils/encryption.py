from cryptography.fernet import Fernet
from flask import current_app

ONE_HOUR = 60 * 60
ONE_DAY = ONE_HOUR * 24
ONE_WEEK = ONE_DAY * 7


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
    fernet = Fernet(KEY)
    return json.loads(fernet.decrypt(token.encode(), ttl=ONE_WEEK).decode())
