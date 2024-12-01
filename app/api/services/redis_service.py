from flask import current_app


def save_session_token(token: str) -> str:
    """Save a session token and return a session ID."""
    import uuid

    breakpoint()
    session_id = str(uuid.uuid4())
    TOKEN_TTL = current_app.config["TOKEN_TTL"]
    REDIS_CLIENT = current_app.config["REDIS_CLIENT"]
    REDIS_CLIENT.set(session_id, token, ex=TOKEN_TTL)
    return session_id


def get_session_token(session_id: str) -> str:
    """Retrieve a session token using the session ID."""
    REDIS_CLIENT = current_app.config["REDIS_CLIENT"]
    return REDIS_CLIENT.get(session_id)
