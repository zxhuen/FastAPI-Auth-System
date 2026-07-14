import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.services.permission import require_admin, require_user 
from app.models.Role import Role
from app.models.User import User    

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def seed_roles(db):
    db.add(Role(name="admin"))
    db.add(Role(name="user"))
    db.commit()

@pytest.fixture
def add_user_for_delete(db):
        user = User(
            username="DeleteMe",
            role_id = 1,
            email="delete@example.com",
            hashed_password="testtestetest"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user.id

@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    def override_require_admin():
        return
    
    def override_require_user():
        return

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[require_admin] = override_require_admin
    app.dependency_overrides[require_user] = override_require_user

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()