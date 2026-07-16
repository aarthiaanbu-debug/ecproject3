import smtplib
from email.message import EmailMessage
from urllib.parse import quote

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import (
    FRONTEND_URL,
    SMTP_FROM_EMAIL,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_USE_TLS,
)
from app.models.user import User
from app.utils.password import hash_password
from app.utils.token import (
    generate_reset_token,
    verify_reset_token
)


def _smtp_configured() -> bool:
    return bool(SMTP_HOST and SMTP_FROM_EMAIL)


def _send_password_reset_email(email: str, reset_url: str) -> None:
    message = EmailMessage()
    message["Subject"] = "Reset your EC APP password"
    message["From"] = SMTP_FROM_EMAIL
    message["To"] = email
    message.set_content(
        "A password reset was requested for your EC APP account.\n\n"
        f"Reset your password here: {reset_url}\n\n"
        "If you did not request this, you can ignore this email."
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
        if SMTP_USE_TLS:
            server.starttls()
        if SMTP_USERNAME and SMTP_PASSWORD:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)


def forgot_password_service(
    db: Session,
    email: str
):

    user = db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user:
        return {
            "message": "If an account exists, a password reset link has been sent"
        }

    token = generate_reset_token(email)
    reset_url = f"{FRONTEND_URL.rstrip('/')}/reset-password?token={quote(token)}"

    if _smtp_configured():
        _send_password_reset_email(email, reset_url)
        return {
            "message": "If an account exists, a password reset link has been sent"
        }

    return {
        "message": "SMTP is not configured; returning reset token for development",
        "reset_token": token,
        "reset_url": reset_url,
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
