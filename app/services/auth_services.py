from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException




def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire

    token = jwt.encode(to_encode, settings.SECRET, settings.ALGORITHM)
    
    return token

def decode_access_token(token: str):

    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Access token has expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )