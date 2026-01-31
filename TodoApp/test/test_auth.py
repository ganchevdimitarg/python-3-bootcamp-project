import pytest

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


def test_create_access_token():
    username = "test_user"
    user_id = "1"
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})

    assert decoded_token["sub"] == username
    assert decoded_token["role"] == role
    assert decoded_token["id"] == user_id


@pytest.mark.asyncio
async def test_get_current_user():
    encode = {"sub": "test_user", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token)
    assert user is not None
    assert user == {"username": "test_user", "id": 1, "role": "admin"}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as ex_info:
        await get_current_user(token)

    assert ex_info.value.status_code == 401
    assert ex_info.value.detail == "Could not validate credentials"


