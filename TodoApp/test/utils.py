import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app
from ..models import Todos, User
from ..routers.user import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///testdb.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"id": 1,"username": "admin", "role": "admin"}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Test",
        description="Test",
        priority=5,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = User(
        username="admin",
        email="user@gmail.com",
        first_name="test",
        last_name="testov",
        hashed_password=bcrypt_context.hash("123"),
        role="user",
        is_active=True,
        phone_number="111111111"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()