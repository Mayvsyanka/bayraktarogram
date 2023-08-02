import enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr
from pydantic.fields import FieldInfo, Undefined, Field

class Role (enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class SortField(str, enum.Enum):
    date = "date"
    rating = "rating"

class UpdateUser(BaseModel):
    bio: str = Field(max_length=500)
    location: str = Field(max_length=100)


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: str
    bio: str = Field(max_length=500)
    location: str = Field(max_length=100)
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    crated_at: datetime
    avatar: str
    bio: str = Field(max_length=500)
    location: str = Field(max_length=100)
    roles: Role

    class Config:
        orm_mode = True

class Profile(BaseModel):
    username: str
    email: str
    crated_at: datetime
    avatar: str
    bio: str = Field(max_length=500)
    location: str = Field(max_length=100)
    images: int

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
    image_id: int

class CommentUpdateModel(BaseModel):
    content: str = Field(max_length=500)
    id: int

class CommentResponse(BaseModel):
    content: str = Field(max_length=500)
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

class RatingModel(BaseModel):
    one_star: Optional[bool] = False
    two_stars: Optional[bool] = False
    three_stars: Optional[bool] = False
    four_stars: Optional[bool] = False
    five_stars: Optional[bool] = False

class RatingResponse(RatingModel):
    id: int = 1
    one_star: bool = False
    two_stars: bool = False
    three_stars: bool = False
    four_stars: bool = False
    five_stars: bool = False
    user_id: int = 1
    image_id: int = 1

    class Config:
        orm_mode = True

class AverageRatingResponse(BaseModel):
    average_rating: float = 0.0
 
    class Config:
        orm_mode = True




