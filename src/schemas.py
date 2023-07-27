import enum
from datetime import datetime
from pydantic import BaseModel, Field

class Role (enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class CommentModel(BaseModel):
    content: str = Field(max_length=250)
    created_at: datetime
    updated_at: datetime
    user_id: int
    user_role: str = Field(max_length=50)
    photo_id = int


class CommentResponse(CommentModel):
    id: int

    class Config:
        orm_mode = True