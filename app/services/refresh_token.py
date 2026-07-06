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

def create_refresh_token(data: dict):
    to_copy = data.copy()
    return  jwt.encode(to_copy, settings.SECRET, settings.ALGORITHM)
    