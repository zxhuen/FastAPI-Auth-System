from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.User import UserCreate, UserResponse, EditUser, user_login, current_user, searchResponse
from app.services.user_services import add_user_services, list_user_services, edit_user_services, delete_user_services, delete_user_pagination_services, login_services, find_user_id_services, get_current_user_session, search_user_services
from uuid import UUID
from app.services.permission import require_user    
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/User", tags=["User"], dependencies=[Depends(require_user)])

@router.post("/")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return add_user_services(db, user)



@router.get("/pagination", response_model=list[UserResponse])
def get_users_pagination(skip: int, limit: int, db: Session = Depends(get_db)):
    return delete_user_pagination_services(db, skip, limit)

@router.get("/getCurretnUser", response_model=current_user)
def get_current_user(token: str, db: Session = Depends(get_db)):
    return get_current_user_session(db, token)

@router.put("/{user_id}", response_model=EditUser)
def edit_user(user_id: UUID, user: EditUser, db: Session = Depends(get_db)):
    users = edit_user_services(db, user_id, user)

    if users is None:
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )   
    
    return users

@router.get("/{username}", response_model=list[searchResponse])
def search_user(username: str, db: Session = Depends(get_db)):
    return search_user_services(db, username)





