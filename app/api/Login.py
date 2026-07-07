from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.User import UserCreate, UserResponse, EditUser, user_login, current_user
from app.services.user_services import add_user_services, list_user_services, edit_user_services, delete_user_services, delete_user_pagination_services, login_services, find_user_id_services, get_current_user_session
from uuid import UUID
from app.services.permission import require_admin
from fastapi.security import OAuth2PasswordRequestForm
from app.services.permission import require_user

router = APIRouter(prefix="/Login", tags=["Login"])

@router.post("/Login")
def validate_account(account: user_login, response: Response, db: Session = Depends(get_db)):
    accountt = user_login(
        username=account.username,
        password=account.password,
    )

    return login_services(db, accountt, response)

@router.post("/LoginOauth")
def validate_account_for_backend(response: Response, account: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    accountt = user_login(
        username=account.username,
        password=account.password
    )

    return login_services(db, accountt, response)