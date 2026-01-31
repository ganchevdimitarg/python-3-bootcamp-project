from fastapi import status

from .utils import *
from ..main import app
from ..routers.DatabaseConnection import get_db
from ..routers.auth import *

app.dependency_overrides[get_db] = override_get_db

def test_auth_user(test_user):
    db = TestingSessionLocal()
    user = auth_user(db, test_user.username, "123")
    assert user is not None
    assert user.username == test_user.username

    non_existent_user = auth_user(db, "wrong_user", "123")
    assert non_existent_user is False

    wrong_password = auth_user(db, test_user.username, "wrong_password")
    assert wrong_password is False