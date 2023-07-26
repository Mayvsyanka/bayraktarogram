import enum
from datetime import datetime
from pydantic import BaseModel, Field

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
    roles: Role

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class RequestEmail(BaseModel):
    email: EmailStr


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class CommentModel(BaseModel):
    content: str = Field(max_length=250)
    created_at: datetime
    updated_at: datetime
    user_id: int
    photo_id: int


class CommentResponse(CommentModel):
    id: int
    #user_id: int

    class Config:
        orm_mode = True
