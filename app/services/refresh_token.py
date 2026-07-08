from sqlalchemy.orm import Session
from app.repository.user_repo import create_user_repo, get_user_repo, edit_user_repo, delete_user_repo, get_user_by_email_repo, get_user_by_username_repo, get_users_pagination_repo, login_repo, find_user_ID_repo, get_current_user_repo
from app.schema.User import UserCreate, UserResponse, EditUser, user_login
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from app.models.User import User
from uuid import UUID
from app.services.auth_services import create_access_token, decode_access_token
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings
from uuid import uuid4
from fastapi import Response
from jose import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from app.repository.refresh_token_repo import check_refresh_token_repo
from app.models.RefreshToken import RefreshToken
from app.services.auth_services import create_access_token

def create_refresh_token(data: dict):
    to_copy = data.copy()
    return  jwt.encode(to_copy, settings.SECRET, settings.ALGORITHM)

def check_refresh_token(refresh_token: str | None):

    if refresh_token is None:
        raise HTTPException(
        status_code=401,
        detail="Missing refresh token"
    )


def decode_refresh_token(refresh_token: str):

    try:
        payload = jwt.decode(refresh_token, settings.SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

def check_refresh_token_from_db(db: Session, jti: UUID):
    refresh_token = check_refresh_token_repo(db, jti)

    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="no refresh token found"
        )
    
    return refresh_token
    
    
def generate_new_refresh_token(user_id: UUID):

    refresh_token_payload = {
    "sub": str(user_id),
    "iat": datetime.now(timezone.utc),
    "exp": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE),
    "jti": str(uuid4()),
    "type": "refresh",
    }

def validate_refresh_token(db: Session, response: Response, refresh_token: str):

    check_refresh_token(refresh_token)

    payload = decode_refresh_token(refresh_token)

    
    
    db_token = check_refresh_token_from_db(db, payload["jti"])

    payload = {
        "sub": payload["sub"]
    }

    new_access_token = create_access_token(payload)

    return payload, db_token, new_access_token
    




    






    