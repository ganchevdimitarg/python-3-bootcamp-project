from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from ..models import Todos
from .DatabaseConnection import db_dependency
from .auth import get_current_user

# dependencies
router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todo", status_code=status.HTTP_200_OK)
async def get_all(user: user_dependency, db: db_dependency):
    if  user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return db.query(Todos).all()

@router.delete("/delete_todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    (db.query(Todos)
     .filter(Todos.id == todo_id)
     .delete())

    db.commit()