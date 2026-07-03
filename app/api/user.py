from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.User import UserCreate, UserResponse, EditUser, user_login, current_user
from app.services.user_services import add_user_services, list_user_services, edit_user_services, delete_user_services, delete_user_pagination_services, login_services, find_user_id_services, get_current_user_session
from uuid import UUID
from app.services.permission import user_role_validation
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/User", tags=["User"])

@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return add_user_services(db, user)

@router.get("/", response_model= list[UserResponse])
def get_user(db: Session = Depends(get_db), current_user = Depends(user_role_validation)):
    return list_user_services(db)

@router.put("/{user_id}", response_model=EditUser)
def edit_user(user_id: UUID, user: EditUser, db: Session = Depends(get_db)):
    users = edit_user_services(db, user_id, user)

    if users is None:
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )   
    
    return users

@router.get("/pagination", response_model=list[UserResponse])
def get_users_pagination(skip: int, limit: int, db: Session = Depends(get_db)):
    return delete_user_pagination_services(db, skip, limit)

@router.get("/getCurretnUser", response_model=current_user)
def get_current_user(token: str, db: Session = Depends(get_db)):
    return get_current_user_session(db, token)

@router.post("/Login")
def validate_account(account: user_login, db: Session = Depends(get_db)):
    accountt = user_login(
        username=account.username,
        password=account.password,
    )

    return login_services(db, accountt)

@router.post("/OauthLogin")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    account = user_login(
        username=form_data.username,
        password=form_data.password,
    )

    return login_services(db, account)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    users = delete_user_services(db, user_id)

    if users is None:
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )
    
    return users


@router.get("/{user_id}", response_model=UserResponse)
def find_user_id(user_id: UUID, db: Session = Depends(get_db)):
    return find_user_id_services(db, user_id)