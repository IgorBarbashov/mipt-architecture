from app.auth import authenticate_user, create_access_token
from app.config import settings
from app.schemas import LoginRequest
from fastapi import FastAPI, HTTPException, Response, status

app = FastAPI(title="Auth Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "auth-service"}


@app.post("/login")
def login(data: LoginRequest, response: Response):
    user = authenticate_user(data.login, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )

    token = create_access_token(user["id"])

    response.set_cookie(
        key=settings.jwt_cookie_name,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/",
        max_age=settings.access_token_expire_minutes * 60,
    )

    return {
        "message": "Login successful",
        "user_id": user["id"],
    }


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=settings.jwt_cookie_name, path="/")
    return {"message": "Logged out"}
