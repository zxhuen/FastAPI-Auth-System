from sqlalchemy.orm import Session
from app.models.User import User
from app.schema.User import UserCreate, UserResponse, EditUser
from uuid import UUID
from pwdlib import PasswordHash
from sqlalchemy.orm import joinedload


password_hash = PasswordHash.recommended()

def create_user_repo(db: Session, Users: User):
    

    db.add(Users)
    db.commit()
    db.refresh(Users)

    return Users

def get_user_repo(db: Session):
    return  (
    db.query(User)
    .options(joinedload(User.role))
    )

def edit_user_repo(db: Session, user_id: UUID, Users: EditUser):
    user_from_db = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user_from_db is None:
        return None
    
    user_from_db.username = Users.username
    user_from_db.email = Users.email    
    

    db.commit()
    db.refresh(user_from_db)

    return user_from_db


def delete_user_repo(db: Session, user_id: UUID):
    user = db.query(User)\
    .options(joinedload(User.role))\
    .filter(User.id == user_id)\
    .first()
    
    db.delete(user)
    db.commit()

    return user

def get_user_by_email_repo(db: Session, user_email: str):
    user = db.query(User).filter(User.email == user_email).first()

    return user

def get_user_by_username_repo(db: Session, user_username: str):
    return db.query(User).filter(User.username == user_username).first()

def get_users_pagination_repo(db: Session, skip: int, limit: int):
    return (
        db.query(User)
        .offset(skip)
        .limit(limit)
        .all()
    )


def login_repo(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def find_user_ID_repo(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_current_user_repo(db: Session, user_id: UUID):
    current_user = (
    db.query(User)
    .options(joinedload(User.role))
    .filter(User.id == user_id)
    .first()
    )


    if current_user is None:
        return None

    
    return current_user

def search_username_repo(db: Session, username: str):
    return db.query(User).filter(User.username.ilike(f"%{username}%")).order_by(User.created_at.desc()).all()