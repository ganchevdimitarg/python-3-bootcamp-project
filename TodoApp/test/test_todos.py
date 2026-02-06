from fastapi import status

from .utils import *
from ..main import app
from ..models import Todos
from ..routers.DatabaseConnection import get_db
from ..routers.auth import get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_auth_users(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Test",
        "description": "Test",
        "priority": 5,
        "complete": False,
        "owner_id": 1,
    }]


def test_get_todo(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Test",
        "description": "Test",
        "priority": 5,
        "complete": False,
        "owner_id": 1,
    }

def test_get_todo_not_found(test_todo):
    response = client.get("/todos/todo/3")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found"}


def test_create_todo(test_todo):
     request_data = {
        "title": "New Test",
        "description": "New Test",
        "priority": 3,
        "complete": True
    }
     response = client.post("/todos/todos", json=request_data)
     assert response.status_code == status.HTTP_201_CREATED

     db = TestingSessionLocal()
     model = db.query(Todos).filter(Todos.id == 2).first()
     assert model.title == request_data["title"]
     assert model.description == request_data["description"]
     assert model.priority == request_data["priority"]
     assert model.complete == request_data["complete"]

def test_update_todo(test_todo):
    request_data = {
        "title": "Update Test",
        "description": "Update Test",
        "priority": 3,
        "complete": True
    }
    response = client.put("/todos/todos/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Update Test"
    assert model.description == "Update Test"

def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Update Test",
        "description": "Update Test",
        "priority": 3,
        "complete": True
    }
    response = client.put("/todos/todos/3", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found"}

def test_delete_todo(test_todo):
    response = client.delete("/todos/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/todos/3")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found"}
