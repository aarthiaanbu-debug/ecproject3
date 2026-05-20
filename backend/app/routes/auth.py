from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User

from app.utils.password import (
    hash_password,
    verify_password
)

from app.utils.jwt_handler import create_token
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

    existing = db.query(User).filter(
        User.email == email
    ).first()

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

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            return {
                "error": "User not found"
            }

        # OLD PLAIN PASSWORD SUPPORT
        if user.password == password:

            token = create_token({
                "sub": user.email,
                "role": user.role
            })

            return {
                "access_token": token,
                "token_type": "bearer",
                "role": user.role
            }

        # HASHED PASSWORD SUPPORT
        if not verify_password(
            password,
            user.password
        ):
            return {
                "error": "Invalid credentials"
            }

        token = create_token({
            "sub": user.email,
            "role": user.role
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": user.role
        }

    except Exception as e:

        return {
            "error": str(e)
        }


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


# =========================
# GOOGLE OAUTH
# =========================

oauth = OAuth()

oauth.register(
    name="google",
    client_id="GOOGLE_CLIENT_ID",
    client_secret="GOOGLE_SECRET",
    server_metadata_url=
    "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)