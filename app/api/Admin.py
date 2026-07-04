from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.User import UserCreate, UserResponse, EditUser, user_login, current_user
from app.services.user_services import add_user_services, list_user_services, edit_user_services, delete_user_services, delete_user_pagination_services, login_services, find_user_id_services, get_current_user_session
from uuid import UUID
from app.services.permission import require_admin
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/Admin", tags=["Admin"], dependencies=[Depends(require_admin)])

@router.get("/", response_model= list[UserResponse])
def get_user(db: Session = Depends(get_db)):
    return list_user_services(db)

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    users = delete_user_services(db, user_id)

    if users is None:
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )
    
    return users


@router.get("/{user_id}", response_model=UserResponse)
def find_user_id(user_id: UUID, db: Session = Depends(get_db)):
    return find_user_id_services(db, user_id)