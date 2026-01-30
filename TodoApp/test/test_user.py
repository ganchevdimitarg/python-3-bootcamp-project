from fastapi import status

from .utils import *
from ..main import app
from ..routers.DatabaseConnection import get_db
from ..routers.UserVerification import UserVerification

from ..routers.user import get_current_user

app.dependency_overrides[get_db] = override_get_db
# app.dependency_overrides[get_current_user] = override_get_current_user

def test_user_info(test_user):
    response = client.get("/user")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "admin"

def test_change_password(test_user):
    response = client.put("/user/password", json={"old_password": "123", "new_password": "999"})

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid(test_user):
    response = client.put("/user/password", json={"old_password": "wrong_password", "new_password": "999"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}

def test_update_phone_number(test_user):
    new_phone = "9998887777"
    response = client.put(f"/user/update-user-info", params={"phone_number": new_phone})
    assert response.status_code == 204
    db = TestingSessionLocal()
    updated_user = db.query(User).filter(User.id == test_user.id).first()
    assert updated_user.phone_number == new_phone
    db.close()
