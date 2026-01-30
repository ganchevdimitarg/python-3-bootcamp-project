from pydantic import BaseModel


class InfoUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool
    role: str
    phone_number: str