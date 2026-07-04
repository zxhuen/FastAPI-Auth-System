from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users")

    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)

    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )