from sqlalchemy.orm import Session
from app.repository.user_repo import create_user_repo, get_user_repo, edit_user_repo, delete_user_repo, get_user_by_email_repo, get_user_by_username_repo, get_users_pagination_repo, login_repo
from app.schema.User import UserCreate, UserResponse, EditUser, user_login
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from app.models.User import User
from uuid import UUID


password_hash = PasswordHash.recommended()

def add_user_services(db: Session, Create: UserCreate):
    existing_email =  get_user_by_email_repo(db, Create.email)

    if existing_email:
        raise HTTPException(
        status_code=409,
        detail="Email already exists."
    )
    
    existing_user = get_user_by_username_repo(db, Create.username)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username already exists."
        )


    try: 
        hashed_password = hash_password(Create.hashed_password)
        
        new_user = User(
            username = Create.username,
            email = Create.email,
            hashed_password = hashed_password
        )

        return create_user_repo(db, new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
        status_code=409,
        detail="Email or Username already exists."
    )

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def list_user_services(db: Session):
    return get_user_repo(db)

def edit_user_services(db: Session, person_id: UUID, user: EditUser):
    return edit_user_repo(db, person_id, user)

def delete_user_services(db: Session, user_id: UUID):
    return delete_user_repo(db, user_id)

def delete_user_pagination_services(db: Session, skip: int, limit: int):
    users = get_users_pagination_repo(db, skip, limit)

    if users is None:
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )
    
    if users == []:
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )
    
    return users

def login_services(db: Session, account: user_login):
    user = login_repo(db, account.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    if not password_hash.verify(account.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return user
    