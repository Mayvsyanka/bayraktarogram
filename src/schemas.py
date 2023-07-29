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
    user_id: int
    image_id: int



class CommentResponse(CommentModel):
    id: int

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


class ImageSettingsModel (BaseModel):  # for Cloudinary
    # relations
    user_id: int = Field(..., example=1)
    image_id: int = Field(..., example=1)
    # url
    url: str = Field(..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")
    secure_url: str = Field(
        ..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")
    transformed_url: str = Field(
        ..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")
    qrcode_url: str = Field(
        ..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")
    # settings
    radius: int = Field(..., example=100)
    effect: str = Field(..., example="sepia")
    width: int = Field(..., example=500)
    height: int = Field(..., example=500)
    crop: str = Field(..., example="fill")
    gravity: str = Field(..., example="face")
    color_space: str = Field(..., example="srgb")
    angle: int = Field(..., example=0)


class ImageSettingsResponseModel (BaseModel):
    user_id: int = Field(..., example=1)
    transformed_url: str = Field(
        ..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")
    qrcode_url: str = Field(
        ..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")

    class Config():
        # This is for Swagger UI documentation
        schema_extra = {
            "example": {
                "user_id": 1,
                "image_url": "https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg"
            }
        }

        orm_mode = True
