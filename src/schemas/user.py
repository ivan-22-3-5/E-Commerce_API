from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    username: str


class UserIn(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
