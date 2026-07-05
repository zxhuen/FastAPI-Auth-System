from sqlalchemy.orm import Session
from app.repository.user_repo import create_user_repo, get_user_repo, edit_user_repo, delete_user_repo, get_user_by_email_repo, get_user_by_username_repo, get_users_pagination_repo, login_repo, find_user_ID_repo, get_current_user_repo
from app.schema.User import UserCreate, UserResponse, EditUser, user_login
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from app.models.User import User
from uuid import UUID
from app.services.auth_services import create_access_token
from app.repository.roles_repo import get_roles_repo


def get_roles_services(db: Session):
    roles =  get_roles_repo(db)

    if not roles:
        raise HTTPException(
            status_code=404,
            detail="no user found"
        )
    
    return roles    