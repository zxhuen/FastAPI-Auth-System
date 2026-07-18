from fastapi import APIRouter, HTTPException, Response, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.User import UserCreate, UserResponse, EditUser, user_login, current_user
from app.services.user_services import add_user_services, list_user_services, edit_user_services, delete_user_services, delete_user_pagination_services, login_services, find_user_id_services, get_current_user_session
from uuid import UUID
from app.services.permission import require_admin
from fastapi.security import OAuth2PasswordRequestForm
from app.services.permission import require_user
from app.services.email_verification import verify_email
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/verify-email")
@limiter.limit("2/minute")
def verify_user_email(request: Request, token: str, db: Session = Depends(get_db)):
    return verify_email(token, db)