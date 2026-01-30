from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from starlette import status

from ..models import User
from .DatabaseConnection import db_dependency
from .InfoUserRequest import InfoUserRequest
from .UserVerification import UserVerification
from .auth import get_current_user

# dependencies
router = APIRouter(
    prefix='/user',
    tags=['user']
)

user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = '3223e6173c1a38deb5af0d78afc48a0a89393e8495a7e4539ef7a4d5e3a75846'
ALGORITHM = 'HS256'


@router.get('/', status_code=status.HTTP_200_OK)
async def user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    auth_user = db.query(User).filter(User.username == user.get('username')).first()

    if auth_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    return InfoUserRequest(
        username=auth_user.username,
        email=auth_user.email,
        first_name=auth_user.first_name,
        last_name=auth_user.last_name,
        hashed_password=auth_user.hashed_password,
        role=auth_user.role,
        is_active=auth_user.is_active,
        phone_number=auth_user.phone_number
    )


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    auth_user = db.query(User).filter(User.id == user.get("id")).first()

    if not bcrypt_context.verify(user_verification.old_password, auth_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password change")

    auth_user.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(auth_user)
    db.commit()

@router.put('/update-user-info', status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str = Path(eq=10)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    auth_user = db.query(User).filter(User.id == user.get("id")).first()

    auth_user.phone_number = phone_number

    db.add(auth_user)
    db.commit()