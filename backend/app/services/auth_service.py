from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.password import hash_password
from app.utils.token import (
    generate_reset_token,
    verify_reset_token
)


def forgot_password_service(
    db: Session,
    email: str
):

    user = db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user:
        return {
            "message": "User not found"
        }

    token = generate_reset_token(email)

    return {
        "reset_token": token
    }


def reset_password_service(
    db: Session,
    token: str,
    new_password: str
):

    email = verify_reset_token(token)

    if not email:
        return {
            "message": "Invalid token"
        }

    user = db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user:
        return {
            "message": "User not found"
        }

    user.password = hash_password(new_password)

    db.commit()

    return {
        "message": "Password updated"
    }
