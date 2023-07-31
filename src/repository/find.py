from sqlalchemy.orm import Session, aliased

from src.database.models import User, Image, Tag
from src.schemas import SortField

async def get_photo_by_tag(tag: str, db:Session, sort_by):
    sort_field = Image.created_at if sort_by == SortField.date else Image.id
    result = db.query(Image).join(
        Image.tags).filter(Tag.name == tag).order_by(sort_field).all()
    return(result)



async def get_photo_by_key_words(words: str, db: Session, sort_by):

    sort_field = Image.created_at if sort_by == SortField.date else Image.id
    images = db.query(Image).filter(Image.description.like(f"%{words}%")).order_by(sort_field).all()
    return images
