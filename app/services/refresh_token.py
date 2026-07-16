from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from fastapi import HTTPException, Response
from jose import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.RefreshToken import RefreshToken
from app.repository.refresh_token_repo import (
    check_refresh_token_repo,
    delete_refresh_token_repo,
    get_user_from_db,
    save_refresh_token,
)
from app.services.auth_services import create_access_token

def create_refresh_token(data: dict):
    to_copy = data.copy()
    return  jwt.encode(to_copy, settings.SECRET, settings.ALGORITHM)

def check_refresh_token(refresh_token: str | None):

    if refresh_token is None:
        raise HTTPException(
        status_code=401,
        detail="Missing refresh token"
    )


def decode_refresh_token(refresh_token: str):

    try:
        payload = jwt.decode(refresh_token, settings.SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

def check_refresh_token_from_db(db: Session, jti: UUID):
    refresh_token = check_refresh_token_repo(db, jti)

    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="no refresh token found"
        )
    
    return refresh_token
    
    
def generate_new_refresh_token(user_id: UUID):

    refresh_token_payload = {
    "sub": str(user_id),
    "iat": datetime.now(timezone.utc),
    "exp": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE),
    "jti": str(uuid4()),
    "type": "refresh",
    }

    return refresh_token_payload

def check_refresh_token_expiration(refresh_token: RefreshToken):

    if refresh_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail="refresh token expired"
        )
    

def delete_old_refresh_token(db: Session, jti: UUID):
    delete_refresh_token_repo(db, jti)


def validate_refresh_token(db: Session, response: Response, refresh_token: str):

    ##validate old token
    check_refresh_token(refresh_token)

    payload = decode_refresh_token(refresh_token)
    jti = UUID(payload["jti"])
    
    
    db_token = check_refresh_token_from_db(db, jti)

    check_refresh_token_expiration(db_token)

    if str(db_token.user_id) != payload["sub"]:
        raise HTTPException(
            status_code=401,
            detail="no person found"
        )

    

    user = get_user_from_db(db, db_token.user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="user not found"
        )

    ##create new refresh token

    new_refresh_token = generate_new_refresh_token(db_token.user_id)

    jwt_refresh_token = create_refresh_token(new_refresh_token)

    

    ##save refresh token to db

    try:
        save_refresh_token(user, new_refresh_token["jti"], new_refresh_token["exp"], db)
        delete_old_refresh_token(db, db_token.jti)
        db.commit()
    except Exception:
        db.rollback()
        raise

    ##set cookie

    response.set_cookie(
    key="refresh_token",
    value=jwt_refresh_token,
    httponly=True,
    secure=False,      # True in production with HTTPS
    samesite="lax",    # or "strict"/"none" depending on your frontend
    max_age=settings.REFRESH_TOKEN_EXPIRE * 24 * 60 * 60,
    )

    access_payload = {
        "sub": payload["sub"]
    }

    new_access_token = create_access_token(access_payload)

    

    return new_access_token
  