from sqlalchemy.orm import Session, aliased
import asyncio
from sqlalchemy import desc, select

from src.database.models import User, Image, Tag, Rating
from src.schemas import SortField
from src.repository.ratings import get_average_rating


async def get_photo_by_tag(tag: str, db: Session, sort_by):
    """
    The get_photo_by_tag function returns a list of images with the given tag.
        The function takes in three arguments:
            - tag: A string representing the name of the tag to search for.
            - db: An instance of Session from SQLAlchemy's ORM, used to query and update data in a database.
            - sort_by: An enum value that determines how to sort returned images (either by date or rating).
    
    :param tag: str: Specify the tag that we want to search for
    :param db: Session: Pass the database session into the function
    :param sort_by: Sort the images by date or rating
    :return: A list of tuples (image, average_rating)
    :doc-author: Trelent
    """
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
    """
    The get_photo_by_key_words function takes in a string of words and returns all images that contain those words.
        The function also takes in a sort_by parameter which can be either SortField.date or SortField.rating,
        and will return the images sorted by date or rating respectively.
    
    :param words: str: Search the database for images with a description that contains the words
    :param db: Session: Pass the database session to the function
    :param sort_by: Sort the images by date or rating
    :return: A list of tuples
    :doc-author: Trelent
    """
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


