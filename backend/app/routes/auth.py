from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import (
    FRONTEND_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_OAUTH_REDIRECT_URL,
)
from app.database import SessionLocal
from app.models.user import User

from app.utils.password import (
    hash_password,
    verify_password
)

from app.utils.jwt_handler import create_refresh_token, create_token, verify_token
from app.services.auth_service import (
    forgot_password_service,
    reset_password_service
)

from authlib.integrations.starlette_client import OAuth


router = APIRouter(tags=["Auth"])


# =========================
# DATABASE
# =========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================
# REGISTER
# =========================

@router.post("/auth/register")
def register(
    name: str,
    email: str,
    password: str,
    role: str = "user",
    db: Session = Depends(get_db)
):

    existing = db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if existing:

        return {
            "error": "Email already exists"
        }

    hashed_password = hash_password(password)

    user = User(
        name=name,
        email=email,
        password=hashed_password,
        role=role
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "message": "User registered successfully"
    }


# =========================
# LOGIN
# =========================

@router.post("/auth/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    try:

        user = db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

        if not user:
            return {
                "error": "User not found"
            }

        # OLD PLAIN PASSWORD SUPPORT
        if user.password == password:

            token_payload = {
                "sub": user.email,
                "role": user.role,
                "user_id": user.id,
                "tenant_id": user.organization_id
            }
            token = create_token(token_payload)
            refresh_token = create_refresh_token(token_payload)

            return {
                "access_token": token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "role": user.role,
                "user": {"id": user.id, "name": user.name, "email": user.email,
                         "tenant_id": user.organization_id}
            }

        # HASHED PASSWORD SUPPORT
        if not verify_password(
            password,
            user.password
        ):
            return {
                "error": "Invalid credentials"
            }

        token_payload = {
            "sub": user.email,
            "role": user.role,
            "user_id": user.id,
            "tenant_id": user.organization_id
        }
        token = create_token(token_payload)
        refresh_token = create_refresh_token(token_payload)

        return {
            "access_token": token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "role": user.role,
            "user": {"id": user.id, "name": user.name, "email": user.email,
                     "tenant_id": user.organization_id}
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Login failed")


# =========================
# FORGOT PASSWORD
# =========================

@router.post("/forgot-password")
def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):

    return forgot_password_service(
        db,
        email
    )


@router.post("/auth/forgot-password")
def forgot_password_alias(
    email: str,
    db: Session = Depends(get_db)
):
    return forgot_password_service(
        db,
        email
    )


# =========================
# RESET PASSWORD
# =========================

@router.post("/reset-password")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):

    return reset_password_service(
        db,
        token,
        new_password
    )


@router.post("/auth/reset-password")
def reset_password_alias(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    return reset_password_service(
        db,
        token,
        new_password
    )


@router.post("/auth/refresh")
def refresh_access_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    token_payload = {
        "sub": payload.get("sub"),
        "role": payload.get("role"),
        "user_id": payload.get("user_id"),
        "tenant_id": payload.get("tenant_id"),
    }
    return {
        "access_token": create_token(token_payload),
        "refresh_token": create_refresh_token(token_payload),
        "token_type": "bearer",
    }


# =========================
# GOOGLE OAUTH
# =========================

oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=
    "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)


@router.get("/auth/google/login")
async def google_login(request: Request):
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=503, detail="Google OAuth is not configured")
    redirect_uri = GOOGLE_OAUTH_REDIRECT_URL or str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback", name="google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token.get("userinfo") or await oauth.google.parse_id_token(request, token)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Google OAuth login failed") from exc

    email = userinfo.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Google account did not provide an email")

    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        user = User(
            name=userinfo.get("name") or email.split("@")[0],
            email=email,
            password=hash_password("google-oauth"),
            role="user",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token_payload = {
        "sub": user.email,
        "role": user.role,
        "user_id": user.id,
        "tenant_id": user.organization_id,
    }
    access_token = create_token(token_payload)
    refresh_token = create_refresh_token(token_payload)
    return RedirectResponse(
        url=(
            f"{FRONTEND_URL.rstrip('/')}/login"
            f"?access_token={access_token}&refresh_token={refresh_token}&role={user.role}"
        )
    )
