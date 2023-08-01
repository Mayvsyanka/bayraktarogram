from sqlalchemy.orm import Session, aliased
import asyncio
from sqlalchemy import desc, select

from src.database.models import User, Image, Tag, Rating
from src.schemas import SortField
from src.repository.ratings import get_average_rating


async def get_photo_by_tag(tag: str, db: Session, sort_by):
    if sort_by == SortField.date:
        sorted_images = db.query(Image).join(Image.tags).filter(Tag.name == tag).order_by(Image.created_at).all()
    else:
        tag = db.execute(select(Tag).filter(Tag.name == tag)).scalar()
        if not tag:
            print(f"Тег '{tag}' не найден.")
            return []

        images_with_ratings = []
        images = tag.images
        for image in images:
            average_rating = await get_average_rating(image.id, db)
            images_with_ratings.append(
                (image, f"average_rating: {average_rating}"))

        sorted_images = sorted(images_with_ratings,
                               key=lambda x: x[1], reverse=True)

    return sorted_images




async def get_photo_by_key_words(words: str, db: Session, sort_by):
    if sort_by == SortField.date:
        query = db.query(Image).filter(Image.description.ilike(
            f"%{words}%")).order_by(Image.created_at)
        sorted_images = query.all()
    else:
        images_with_ratings = []
        images = db.query(Image).filter(Image.description.ilike(f"%{words}%")).all()
        for image in images:
            average_rating = await get_average_rating(image.id, db)
            images_with_ratings.append((image, average_rating))

        sorted_images = sorted(images_with_ratings,
                               key=lambda x: x[1], reverse=True)

    return sorted_images


