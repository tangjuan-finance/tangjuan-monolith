from app import redis_client


def save_session_token(token: str) -> str:
    """Save a session token and return a session ID."""
    import uuid

    session_id = str(uuid.uuid4())
    redis_client.set(session_id, token, ex=3600)  # Expiry: 1 hour
    return session_id


def get_session_token(session_id: str) -> str:
    """Retrieve a session token using the session ID."""
    return redis_client.get(session_id)
