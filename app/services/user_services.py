import logging
from sqlalchemy.orm import Session
from app.repository.user_repo import (
    create_user_repo,
    get_user_repo,
    edit_user_repo,
    delete_user_repo,
    get_user_by_email_repo,
    get_user_by_username_repo,
    get_users_pagination_repo,
    login_repo,
    find_user_ID_repo,
    get_current_user_repo,
    search_username_repo,
)
from app.schema.User import UserCreate, UserResponse, EditUser, user_login
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from app.models.User import User
from uuid import UUID
from app.services.auth_services import create_access_token, decode_access_token
from app.services.refresh_token import create_refresh_token
from app.repository.refresh_token_repo import save_refresh_token
from fastapi import Depends
from app.core.database import get_db
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from uuid import uuid4
from fastapi import Response
from app.services.email_verification import (
    generate_verification_token,
    send_verification_email,
)

logger = logging.getLogger(__name__)


password_hash = PasswordHash.recommended()


def add_user_services(db: Session, Create: UserCreate):
    logger.info(
        "Registering user with username=%s email=%s",
        Create.username,
        Create.email,
    )

    existing_email = get_user_by_email_repo(db, Create.email)

    if existing_email:
        logger.warning("Registration failed: email already exists (%s)", Create.email)
        raise HTTPException(
            status_code=409,
            detail="Email already exists."
        )

    existing_user = get_user_by_username_repo(db, Create.username)

    if existing_user:
        logger.warning(
            "Registration failed: username already exists (%s)",
            Create.username,
        )
        raise HTTPException(
            status_code=409,
            detail="Username already exists."
        )

    try:
        hashed_password = hash_password(Create.hashed_password)

        new_user = User(
            role_id=2,
            username=Create.username,
            email=Create.email,
            hashed_password=hashed_password
        )

        user = create_user_repo(db, new_user)
        logger.info("User created successfully. user_id=%s", user.id)

        verification_token = generate_verification_token(user.id)
        send_verification_email(user.email, verification_token)

        logger.info("Verification email sent to %s", user.email)

        return {
            "message": "Registration successfully."
        }

    except IntegrityError:
        logger.exception("IntegrityError while creating user")
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email or Username already exists."
        )


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def list_user_services(db: Session):
    return get_user_repo(db)


def edit_user_services(db: Session, person_id: UUID, user: EditUser):
    logger.info("Editing user %s", person_id)
    return edit_user_repo(db, person_id, user)


def delete_user_services(db: Session, user_id: UUID):
    logger.info("Deleting user %s", user_id)

    user = delete_user_repo(db, user_id)

    if user is None:
        logger.warning("Delete failed. User not found: %s", user_id)
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    logger.info("User deleted successfully: %s", user_id)
    return user


def delete_user_pagination_services(db: Session, skip: int, limit: int):
    logger.info("Fetching users with pagination skip=%s limit=%s", skip, limit)

    users = get_users_pagination_repo(db, skip, limit)

    if users is None:
        logger.warning("Pagination returned None")
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )

    if users == []:
        logger.warning("Pagination returned empty list")
        raise HTTPException(
            status_code=404,
            detail="no person found"
        )

    logger.info("Retrieved %d users", len(users))
    return users


def login_services(db: Session, account: user_login, response: Response):
    logger.info("Login attempt for username=%s", account.username)

    user = login_repo(db, account.username)

    if user is None:
        logger.warning("Login failed. User not found: %s", account.username)
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not password_hash.verify(account.password, user.hashed_password):
        logger.warning("Login failed. Invalid password for %s", account.username)
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token_data = {
        "sub": str(user.id)
    }

    generated_user_token = create_access_token(token_data)

    refresh_token_payload = {
        "sub": str(user.id),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE),
        "jti": str(uuid4()),
        "type": "refresh",
    }

    refresh_token = create_refresh_token(refresh_token_payload)

    save_refresh_token(
        user,
        refresh_token_payload["jti"],
        refresh_token_payload["exp"],
        db,
    )
    db.commit()

    logger.info("Refresh token saved for user_id=%s", user.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 30
    )

    logger.info("Login successful for user_id=%s", user.id)

    payload = {
        "access_token": generated_user_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

    return payload


def find_user_id_services(db: Session, user_id: UUID):
    logger.info("Finding user by id=%s", user_id)

    user = find_user_ID_repo(db, user_id)

    if user is None:
        logger.warning("User not found: %s", user_id)
        raise HTTPException(
            status_code=401,
            detail="no user found"
        )

    logger.info("User found: %s", user_id)
    return user


def get_current_user_session(db: Session, token: str):
    logger.info("Getting current user from access token")

    validated_token = decode_access_token(token)

    current_user = get_current_user_repo(
        db,
        UUID(validated_token["sub"])
    )

    if current_user is None:
        logger.warning("Current user not found")
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    logger.info("Current user retrieved: %s", current_user.id)
    return current_user


def search_user_services(db: Session, username: str):
    logger.info("Searching users with username=%s", username)

    users = search_username_repo(db, username)

    if not users:
        logger.warning("Search returned no users for username=%s", username)
        raise HTTPException(
            status_code=401,
            detail="user not found"
        )

    logger.info("Search returned %d user(s)", len(users))
    return users