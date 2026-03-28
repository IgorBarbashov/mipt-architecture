from datetime import datetime, timedelta, timezone

import jwt
from app.config import settings
from app.storage import USERS


def authenticate_user(login: str, password: str):
    for user in USERS:
        if user["login"] == login and user["password"] == password:
            return user
    return None


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": user_id,
        "exp": expire,
    }

    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token
