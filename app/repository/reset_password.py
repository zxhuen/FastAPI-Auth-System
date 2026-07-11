from app.models.Role import Role
from sqlalchemy.orm import Session
from app.models.User import User
from app.schema.User import UserCreate, UserResponse, EditUser
from uuid import UUID
from pwdlib import PasswordHash
from sqlalchemy.orm import joinedload
from app.models.resetPassword import PasswordResetToken


def get_user_through_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_token(db: Session, token: str):
    return db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()