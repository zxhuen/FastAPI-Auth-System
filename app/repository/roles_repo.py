from app.models.Role import Role
from sqlalchemy.orm import Session
from app.models.User import User
from app.schema.User import UserCreate, UserResponse, EditUser
from uuid import UUID
from pwdlib import PasswordHash
from sqlalchemy.orm import joinedload

def get_roles_repo(db: Session):
    return db.query(Role).all()
