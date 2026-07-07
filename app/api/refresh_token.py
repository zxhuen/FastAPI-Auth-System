from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.User import UserCreate, UserResponse, EditUser, user_login, current_user
from app.services.user_services import add_user_services, list_user_services, edit_user_services, delete_user_services, delete_user_pagination_services, login_services, find_user_id_services, get_current_user_session
from uuid import UUID
from app.services.permission import require_admin
from fastapi.security import OAuth2PasswordRequestForm
from app.services.permission import require_user

router = APIRouter(prefix="/Refresh", tags=["Refresh"])