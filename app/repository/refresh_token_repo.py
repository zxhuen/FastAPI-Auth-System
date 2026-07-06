from sqlalchemy.orm import Session
from app.models.User import User
from app.schema.User import UserCreate, UserResponse, EditUser
from uuid import UUID
from pwdlib import PasswordHash
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, timezone
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