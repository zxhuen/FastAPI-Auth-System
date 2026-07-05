from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.services.user_services import get_current_user_session
from app.core.security import oauth2_scheme
from app.core.database import get_db

def require_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user_session(db, token)

    role = current_user.role.name

    if role != "admin":
        raise HTTPException(
            status_code=401,
            detail="forbidden"
        )
    
    return role


def require_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user_session(db, token)

    role = current_user.role.name

    if role not in("user", "admin"):
        raise HTTPException(
            status_code=401,
            detail="forbidden"
        )
    
    return role
    