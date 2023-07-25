import enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

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
    user_role: str = Field(max_length=50)
    photo_id = int


class CommentResponse(CommentModel):
    id: int
    #user_id: int

    class Config:
        orm_mode = True

class TagModel(BaseModel):
    name: str = Field(max_length=25)

class TagResponse(TagModel):
    id: int = 1
    name: str

    class Config:
        orm_mode = True

class ImageAddModel(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[str]]

class ImageAddTagModel(BaseModel):
    tags: Optional[List[str]]

class ImageUpdateModel(BaseModel):
    description: str = Field(max_length=500)

class ImageDb(BaseModel):
    id: int
    url: str
    description: str
    tags: List[TagResponse]
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        exclude = {'updated_at', 'user', 'public_name'}

class ImageGetResponse(BaseModel):
    image: ImageDb
    comments: List[CommentResponse]

class ImageAddResponse(BaseModel):
    image: ImageDb
    detail: str = "Image was successfully added"

    class Config:
        orm_mode = True

class ImageUpdateDescrResponse(BaseModel):
    id: int
    description: str
    detail: str = "Image was successfully updated"

    class Config:
        orm_mode = True

class ImageDeleteResponse(BaseModel):
    image: ImageDb
    detail: str = "Image was successfully deleted"

class ImageAddTagResponse(BaseModel):
    id: int
    tags: List[TagResponse]
    detail: str = "Image was successfully updated"

    class Config:
        orm_mode = True

class ImageGetAllResponse(BaseModel):
    images: List[ImageGetResponse]


