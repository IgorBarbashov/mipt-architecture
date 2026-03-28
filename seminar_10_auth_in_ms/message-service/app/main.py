from fastapi import FastAPI, HTTPException, Request, status
from jwt import ExpiredSignatureError, InvalidTokenError

from app.auth import validate_token
from app.config import settings
from app.schemas import MessageRequest

app = FastAPI(title="Message Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "message-service"}


@app.post("/messages", status_code=status.HTTP_201_CREATED)
def create_message(data: MessageRequest, request: Request):
    token = request.cookies.get(settings.jwt_cookie_name)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing auth cookie",
        )

    try:
        payload = validate_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user_id = payload["sub"]

    return {
        "message": "Message created",
        "user_id": user_id,
        "text": data.text,
    }
