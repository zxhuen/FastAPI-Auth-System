from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.User import UserCreate, UserResponse, EditUser
from app.services.user_services import add_user_services, list_user_services, edit_user_services, delete_user_services, delete_user_pagination_services
from uuid import UUID

router = APIRouter(prefix="/User", tags=["User"])

@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return add_user_services(db, user)

@router.get("/", response_model= list[UserResponse])
def get_user(db: Session = Depends(get_db)):
    return list_user_services(db)

@router.put("/{user_id}", response_model=EditUser)
def edit_user(user_id: UUID, user: EditUser, db: Session = Depends(get_db)):
    users = edit_user_services(db, user_id, user)

    if users is None:
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )   
    
    return users

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    users = delete_user_services(db, user_id)

    if users is None:
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )
    
    return users

@router.get("/pagination", response_model=list[UserResponse])
def get_users_pagination(skip: int, limit: int, db: Session = Depends(get_db)):
    return delete_user_pagination_services(db, skip, limit)
    