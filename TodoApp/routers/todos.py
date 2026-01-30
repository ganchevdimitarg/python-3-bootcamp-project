from typing import Annotated, Any

from fastapi import  HTTPException, Path, APIRouter
from fastapi.params import Depends
from starlette import status

from ..models import Todos
from ..TodoRequest import TodoRequest
from .DatabaseConnection import db_dependency
from .auth import get_current_user

router = APIRouter()
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/")
async def get_user_todos(user: user_dependency, db: db_dependency):
    has_auth_user(user)
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    has_auth_user(user)
    todo_model = checks_user_todos_by_id(db, todo_id, user)
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todos(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    has_auth_user(user)
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todos(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    has_auth_user(user)
    todo_model = checks_user_todos_by_id(db, todo_id, user)
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.complete = todo_request.complete
    todo_model.priority = todo_request.priority

    db.add(todo_model)
    db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    has_auth_user(user)
    todo_model = checks_user_todos_by_id(db, todo_id, user)
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    (db.query(Todos)
     .filter(Todos.id == todo_id)
     .filter(Todos.owner_id == user.get("id"))
     .delete())

    db.commit()


def has_auth_user(user: dict):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")


def checks_user_todos_by_id(db, todo_id: int, user: dict) -> Any:
    return (db.query(Todos)
            .filter(Todos.id == todo_id)
            .filter(Todos.owner_id == user.get("id"))
            .first())
