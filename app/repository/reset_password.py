from app.models.Role import Role
from sqlalchemy.orm import Session
from app.models.User import User
from app.schema.User import UserCreate, UserResponse, EditUser
from uuid import UUID
from pwdlib import PasswordHash
from sqlalchemy.orm import joinedload
from app.repository.reset_password import get_user_through_email

def get_user_through_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()