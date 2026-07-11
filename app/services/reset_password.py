from sqlalchemy.orm import Session
from app.repository.user_repo import create_user_repo, get_user_repo, edit_user_repo, delete_user_repo, get_user_by_email_repo, get_user_by_username_repo, get_users_pagination_repo, login_repo, find_user_ID_repo, get_current_user_repo, search_username_repo
from app.schema.User import UserCreate, UserResponse, EditUser, user_login
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
from app.repository.reset_password import get_user_through_email
from jose import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import secrets
from app.models.resetPassword import PasswordResetToken
import hashlib



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

    

    
