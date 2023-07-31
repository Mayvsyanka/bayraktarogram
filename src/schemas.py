import enum
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, EmailStr
from pydantic.fields import FieldInfo, Undefined, Field

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


class ImageSettingsModel(BaseModel): # POST
    # relations
    # id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    image_id: int = Field(..., example=1)

    transformation: List[Dict[str, str]] = Field(..., example=[{"radius": "max"}, {"effect": "sepia"}, {"width": "500"}, {"height": "500"}, {"crop": "fill"}, {"gravity": "face"}, {"color_space": "srgb"}, {"angle": "0"}])    
   
class ImageSettingsResponseModel(BaseModel): 
    id: int = Field(..., example=1)
    transformed_url: str = Field(..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")
    # qrcode_url: str = Field(..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")
    class Config():
        orm_mode = True 
        
        
class ImageSettingsQrcodeResponseModel(BaseModel): 
    id: int = Field(..., example=1)
    # transformed_url: str = Field(..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")
    qrcode_url: str = Field(..., example="https://res.cloudinary.com/dhjzilr2j/image/upload/v1626406216/quickstart_butterfly.jpg")
    class Config():
        orm_mode = True       


