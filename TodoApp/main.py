from fastapi import FastAPI

from .models import Base
from .database import engine
from .routers import auth, todos, admin, user
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy", status_code=200)
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)

# DELETED
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# db_dependency = Annotated[SessionLocal, Depends(get_db)]
# @app.get("/")
# async def get_todos(db: db_dependency):
#     return db.query(Todos).all()
#
# @app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
# async def get_todos(db: db_dependency, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#
# @app.post("/todos", status_code=status.HTTP_201_CREATED)
# async def create_todos(db: db_dependency, todo_request: TodoRequest):
#     todo_model = Todos(**todo_request.model_dump())
#     db.add(todo_model)
#     db.commit()
#
# @app.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def update_todos(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#
#     todo_model.title = todo_request.title
#     todo_model.description = todo_request.description
#     todo_model.completed = todo_request.completed
#     todo_model.priority = todo_request.priority
#
#     db.add(todo_model)
#     db.commit()
#
# @app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todos(db: db_dependency, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     db.query(Todos).filter(Todos.id == todo_id).delete()
#
#     db.commit()