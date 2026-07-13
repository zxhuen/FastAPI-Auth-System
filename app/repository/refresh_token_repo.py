from sqlalchemy.orm import Session
from app.models.User import User
from app.schema.User import UserCreate, UserResponse, EditUser
from uuid import UUID
from pwdlib import PasswordHash
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, timezone
from app.models.RefreshToken import RefreshToken
from app.models.RefreshToken import RefreshToken
from fastapi import HTTPException

def save_refresh_token(user: User, jti: UUID, expires_at: datetime, db: Session):
    refresh_token = RefreshToken(
        user_id = user.id,
        jti = UUID(jti),
        expires_at = expires_at
    )

    db.add(refresh_token)
    

def check_refresh_token_repo(db: Session, jti: UUID):
    return db.query(RefreshToken).filter(RefreshToken.jti == jti).first()

def delete_refresh_token_repo(db: Session, jti: UUID):
    token = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()

    if token is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    db.delete(token)

def get_user_from_db(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()