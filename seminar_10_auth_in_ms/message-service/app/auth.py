import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.config import settings


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )

    if "sub" not in payload:
        raise InvalidTokenError("Missing sub claim")

    return payload


def validate_token(token: str) -> dict:
    try:
        return decode_access_token(token)
    except ExpiredSignatureError:
        raise
    except InvalidTokenError:
        raise
