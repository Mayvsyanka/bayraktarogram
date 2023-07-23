import enum

from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr

class Role (enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)

class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str
    role: str = Field(default="user")

    class Config:
        orm_mode = True


class FirstUserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str
    role: str = Field(default="admin")

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
