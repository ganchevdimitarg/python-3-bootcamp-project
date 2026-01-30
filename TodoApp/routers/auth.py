from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette import status
from jose import jwt

from ..models import User
from .CreateUserRequest import CreateUserRequest
from .DatabaseConnection import db_dependency
from .Token import Token

# dependencies
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = '3223e6173c1a38deb5af0d78afc48a0a89393e8495a7e4539ef7a4d5e3a75846'
ALGORITHM = 'HS256'

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_users(db: db_dependency, user_request: CreateUserRequest):
    user_model = User(
        username=user_request.username,
        email=user_request.email,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        is_active=True,
        phone_number=user_request.phone_number
    )

    db.add(user_model)
    db.commit()
    return user_model


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = auth_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=10))

    return {"access_token": token, "token_type": "bearer"}


def auth_user(db, username, password):
    user = (db.query(User).filter(User.username == username).first())
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user

def create_access_token(username: str, user_id: str, role: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": int(expires.timestamp())})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        role: str = payload.get("role")
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {"username": username, "id": user_id, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")



