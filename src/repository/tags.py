from typing import List, Type

from sqlalchemy.orm import Session

from src.database.models import Tag
from src.schemas import TagModel

async def create_tag(body: TagModel, db: Session) -> Tag:
    """
    The create_tag function creates a new tag in the database.

    :param body: TagModel: Define the body of the request
    :param db: Session: Access the database
    :return: A tag object
    """

    tag = Tag(name=body.name.lower())
    db.add(tag)
    db.commit()
    db.refresh(tag)
   
    return tag

async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    """
    The update_tag function updates a tag in the database.
        Args:
            tag_id (int): The id of the tag to update.
            body (TagModel): The new name for the Tag object.

    :param tag_id: int: Identify the tag to be deleted
    :param body: TagModel: Get the new name of the tag
    :param db: Session: Access the database
    :return: The updated tag or none if the tag does not exist
    """

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        new_tag_in_base = db.query(Tag).filter(Tag.name == body.name.lower()).first()
        if new_tag_in_base:
            return None
        tag.name = body.name.lower()
        db.commit()

    return tag

async def delete_tag(tag_id: int, db: Session) -> Tag | None:
    """
    The delete_tag function deletes a tag from the database.

    :param tag_id: int: Specify the id of the tag to be deleted
    :param db: Session: Pass in the database session
    :return: The deleted tag
    """

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()

    return tag

async def get_tags(skip: int, limit: int, db: Session) -> List[Type[Tag]]:
    """
    The get_tags function returns a list of tags from the database.

    :param skip: int: Skip the first n tags
    :param limit: int: Limit the number of tags returned
    :param db: Session: Pass the database session to the function
    :return: A list of tags
    """

    return db.query(Tag).offset(skip).limit(limit).all()

async def get_tag(tag_id: int, db: Session) -> Type[Tag] | None:
    
    return db.query(Tag).filter(Tag.id == tag_id).first()


