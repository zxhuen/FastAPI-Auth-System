from sqlalchemy.orm import Session
from app.repository.user_repo import get_current_user_repo

from fastapi import HTTPException


from app.models.User import User
from uuid import UUID
from fastapi import Depends
from app.core.database import get_db
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from uuid import uuid4
from fastapi import Response
from jose import jwt, ExpiredSignatureError, JWTError
import resend


resend.api_key = settings.RESEND_API_KEY

def generate_verification_token(user_id: UUID):

    payload = {
        "sub": str(user_id),
        "type": "email-verification",
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    token = jwt.encode(
        payload,
        settings.SECRET,
        algorithm=settings.ALGORITHM
    )

    return token

def verify_email(token: str, db: Session):
    try:
        decoded_payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=400,
            detail="expired token"
        )
    except JWTError:
        raise HTTPException(
            status_code=400,
            detail="invalid token"
        )

    if decoded_payload.get("type") != "email-verification":
        raise HTTPException(
            status_code=400,
            detail="Invalid verification token"
        )
    
    user = get_current_user_repo(db, UUID(decoded_payload["sub"]))
    
    if user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="User is already verified."
        )
    
    try:
        user.is_verified = True

        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    return {"detail": "Verification successful."}
    

def send_verification_email(email: str, token: str):
    verification_link = (
        f"http://localhost:8000/auth/verify-email?token={token}"
    )

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": [email],
        "subject": "Verify your email",
        "html": f"""
        <h2>Welcome!</h2>

        <p>Thanks for registering.</p>

        <p>
            <a href="{verification_link}">
                Verify Email
            </a>
        </p>

        <p>This link expires in 24 hours.</p>
        """
    })


    



