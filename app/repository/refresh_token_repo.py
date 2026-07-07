from sqlalchemy.orm import Session
from app.models.User import User
from app.schema.User import UserCreate, UserResponse, EditUser
from uuid import UUID
from pwdlib import PasswordHash
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, timezone
from app.models.RefreshToken import RefreshToken
from app.models.RefreshToken import RefreshToken

def save_refresh_token(user: User, jti: UUID, expires_at: datetime, db: Session):
    refresh_token = RefreshToken(
        user_id = user.id,
        jti = jti,
        expires_at = expires_at
    )

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

def check_refresh_token_repo(db: Session, id: int, user_id: int):
    return db.query(RefreshToken).filter(RefreshToken.id == id & RefreshToken.user_id == user_id).first()