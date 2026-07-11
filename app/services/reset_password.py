from sqlalchemy.orm import Session
from app.repository.user_repo import create_user_repo, get_user_repo, edit_user_repo, delete_user_repo, get_user_by_email_repo, get_user_by_username_repo, get_users_pagination_repo, login_repo, find_user_ID_repo, get_current_user_repo, search_username_repo
from app.schema.User import UserCreate, UserResponse, EditUser, user_login, reset_password
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from app.models.User import User
from uuid import UUID
from app.services.auth_services import create_access_token, decode_access_token
from app.services.refresh_token import create_refresh_token
from app.repository.refresh_token_repo import save_refresh_token
from fastapi import Depends
from app.core.database import get_db
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from uuid import uuid4
from fastapi import Response
from app.services.email_verification import generate_verification_token, send_verification_email
from app.repository.reset_password import get_user_through_email, get_token
from jose import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import secrets
from app.models.resetPassword import PasswordResetToken
import hashlib
import resend

resend.api_key = settings.RESEND_API_KEY

def forgot_password(db: Session, email: str):
    user = get_user_through_email(db, email)

    if user is None:
        return

    token = secrets.token_urlsafe(32)

    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    reset_token = PasswordResetToken(
        user_id = user.id,
        token = hashed_token,
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    )

    db.add(reset_token)
    db.commit()

    return token

def send_email(email: str, token: str):
    link = f"http://localhost:8000/auth/validate_token?token={token}"

    resend.Emails.send({
        "from": "zxhuen324@gmail.dev",
        "to": [email],
        "subject": "Reset your password",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; line-height: 1.6;">
            <h2>Password Reset Request</h2>

            <p>Hello,</p>

            <p>
                We received a request to reset your password. Click the button
                below to choose a new password.
            </p>

            <p style="margin: 30px 0;">
                <a href="{link}"
                   style="
                        background-color: #2563eb;
                        color: #ffffff;
                        text-decoration: none;
                        padding: 12px 24px;
                        border-radius: 6px;
                        display: inline-block;
                        font-weight: bold;
                   ">
                    Reset Password
                </a>
            </p>

            <p>
                This link will expire in <strong>30 minutes</strong>.
            </p>

            <p>
                If you didn't request a password reset, you can safely ignore
                this email. Your password will remain unchanged.
            </p>

            <hr style="margin: 30px 0;">

            <p style="font-size: 14px; color: #666;">
                If the button doesn't work, copy and paste this URL into your browser:
            </p>

            <p style="font-size: 14px; word-break: break-all;">
                {link}
            </p>
        </div>
        """
    })

def password_reset_verification(db: Session, token: str):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    token_from_db = get_token(db, hashed_token)

    if token_from_db is None:
        raise HTTPException(
            detail="invalid token"
        )
    
    if token_from_db.used is True:
        raise HTTPException(
            detail="token has already been used"
        )

    if token_from_db.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
        status_code=400,
        detail="Reset token has expired."
    )

    return {"message": "proceed to reset password and put this token there" + token_from_db.token}

##def password_reset(token: str, db: Session)





    

    
