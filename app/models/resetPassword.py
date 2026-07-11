from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID, ForeignKey, func
from app.core.database import Base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone, timedelta

class PasswordResetToken(Base):
    __tablename__ = "password_Reset_token"

    id = Column(Integer, primary_key=True)

    user_id = Column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False
    )

    token = Column(String, unique=True, nullable=False)
    expires_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=30),
        nullable=False
    )
    used = Column(Boolean, nullable=False, default=False)

    user = relationship("User")