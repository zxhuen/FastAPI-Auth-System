from app.models.Role import Role
from sqlalchemy.orm import Session
from app.models.User import User
from app.schema.User import UserCreate, UserResponse, EditUser
from uuid import UUID
from pwdlib import PasswordHash
from sqlalchemy.orm import joinedload
from app.models.resetPassword import PasswordResetToken
from app.models.RefreshToken import RefreshToken

def get_user_through_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_token(db: Session, token: str):
    return db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()

def remove_duplicate(db: Session, user_id: UUID):
    db.query(PasswordResetToken).filter(
    PasswordResetToken.user_id == user_id
    ).delete()

def delete_refresh_tokens(db: Session, user_id: UUID):
    db.query(RefreshToken).filter(
    RefreshToken.user_id == user_id
    ).delete()