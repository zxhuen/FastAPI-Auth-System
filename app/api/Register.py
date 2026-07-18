from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.User import UserCreate, UserResponse, EditUser, user_login, current_user, searchResponse
from app.services.user_services import add_user_services, list_user_services, edit_user_services, delete_user_services, delete_user_pagination_services, login_services, find_user_id_services, get_current_user_session, search_user_services
from uuid import UUID
from app.services.permission import require_user    
from fastapi.security import OAuth2PasswordRequestForm
from app.core.limiter import limiter

router = APIRouter(prefix="/Register", tags=["Register"])

@router.post("/", status_code=201)
@limiter.limit("2/minute")
def add_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    return add_user_services(db, user)