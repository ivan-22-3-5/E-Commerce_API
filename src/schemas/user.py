from pydantic import BaseModel, EmailStr, field_validator

from src.utils import hash_pass


class UserIn(BaseModel):
    email: EmailStr
    password: str
    username: str

    @field_validator('password', mode='after')
    @classmethod
    def hash_password(cls, password) -> str:
        return hash_pass(password)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
