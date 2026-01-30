from fastapi import status

from .utils import *
from ..main import app
from ..models import Todos
from ..routers.DatabaseConnection import get_db
from ..routers.admin import get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_all():
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK


def test_delete_todo(test_todo):
    response = client.delete("/admin/delete_todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/admin/delete_todos/3")
    assert response.status_code == status.HTTP_404_NOT_FOUND