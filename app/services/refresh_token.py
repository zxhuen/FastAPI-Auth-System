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

def create_refresh_token(data: dict):
    to_copy = data.copy()
    return  jwt.encode(to_copy, settings.SECRET, settings.ALGORITHM)

def check_refresh_token(refresh_token: str):

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
            detail="Access token has expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )

def check_refresh_token_from_db(refresh_token: str):

def generate_new_refresh_token(db: Session, response: Response, refresh_token: str):

    check_refresh_token(refresh_token)
    decoded_refresh_token = decode_refresh_token(refresh_token)




    