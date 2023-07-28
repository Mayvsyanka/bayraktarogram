from datetime import datetime
from collections import OrderedDict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Image, User, Tag, Comment
from src.schemas import ImageUpdateModel, ImageAddModel, ImageAddTagModel, Role


async def add_image(db: Session, image: ImageAddModel, tags: list[str], url: str, public_name: str, user: User):
    """
    The add_image function adds an image to the database.
        Args:
            db (Session): The database session object.
            image (ImageAddModel): The ImageAddModel object containing the description of the new image. 
            tags (list[str]): A list of strings representing tags for this new image.  Each tag must be less than 25 characters long, and there can only be five tags per image at most.   If more than five are provided, only the first five will be used and a message will be returned indicating that this has happened so that it can be displayed to users on their screen if they

    :param db: Session: Access the database
    :param image: ImageAddModel: Create a new image object
    :param tags: list[str]: Pass in a list of tags
    :param url: str: Store the url of the image in the database
    :param public_name: str: Store the name of the image file
    :param user: User: Get the user id of the image's creator
    :return: A tuple of the image and a message
    """

    if not user:
        return None

    num_tags = 0
    image_tags = []
    for tag in tags:
        if len(tag) > 25:
            tag = tag[0:25]
        if not db.query(Tag).filter(Tag.name == tag.lower()).first():
            db_tag = Tag(name=tag.lower())
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
    
        if num_tags < 5:
            image_tags.append(tag.lower())
        num_tags += 1
    message = ""

    if num_tags >= 5:
        message = "Only five tags can be added to an image"

    tags = db.query(Tag).filter(Tag.name.in_(image_tags)).all()
    db_image = Image(description=image.description, tags=tags, url=url, public_name=public_name, user_id=user.id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
 
    return db_image, message


async def update_image(db: Session, image_id, image: ImageUpdateModel, user: User):
    """
    The update_image function updates the description of an image.
        Args:
            db (Session): The database session object.
            image_id (int): The id of the image to be updated.
            image (ImageUpdateModel): An ImageUpdateModel object containing the new description for this particular 

    :param db: Session: Access the database
    :param image_id: Identify the image to be deleted
    :param image: ImageUpdateModel: Get the new description for the image
    :param user: User: Check if the user is an admin or not
    :return: An image object
    """

    if user.roles == Role.admin:
        db_image = db.query(Image).filter(Image.id == image_id).first()
    else:
        db_image = db.query(Image).filter(Image.id == image_id, Image.user_id == user.id).first()

    if db_image:
        db_image.description = image.description
        db.commit()
        db.refresh(db_image)
        return db_image
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    

async def delete_image(db: Session, id: int, user: User):
    """
    The delete_image function deletes an image from the database.
        Args:
            db (Session): The database session object.
            id (int): The ID of the image to be deleted.

    :param db: Session: Access the database
    :param id: int: Specify which image to delete
    :param user: User: Check if the user is an admin or not
    :return: A database object
    """

    if user.roles == Role.admin:
        db_image = db.query(Image).filter(Image.id == id).first()
    else:
        db_image = db.query(Image).filter(Image.id == id, Image.user_id == user.id).first()

    if db_image:
        db.delete(db_image)
        db.commit()
        return db_image
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def normalize_tags(body):
    """
    The normalize_tags function takes a list of tags and returns a list of unique, trimmed tags.
        The function first splits the tag strings by commas, then trims each tag to 25 characters.
        It then removes duplicate tags from the list using an OrderedDict object.

    :param body: Get the tags from the body of a post
    :return: A list of tags, which are strings
    """

    tags = [tag[:25].strip() for tag_str in body.tags for tag in tag_str.split(",") if tag]
    correct_tags = list(OrderedDict.fromkeys(tags))

    return correct_tags


async def add_tag(db: Session, image_id, body: ImageAddTagModel, user: User):
    """
    The add_tag function adds tags to an image.
        Args:
            db (Session): The database session object.
            image_id (int): The id of the image to add tags to.
            body (ImageAddTagModel): A model containing the tag names in a list format, as well as a boolean value for whether or not the user wants their new tags added on top of existing ones or replacing them entirely.  This is passed in from the request body and validated by pydantic before being passed into this function.  If it fails validation, an HTTPException will be raised with status code 400 and details

    :param db: Session: Access the database
    :param image_id: Identify the image in the database
    :param body: ImageAddTagModel: Pass the tags to be added to the image
    :param user: User: Check if the user is an admin or not
    :return: The image object and a detail string
    """

    tags = await normalize_tags(body)

    num_tags = 0
    list_tags = []
    detail = ""
    for tag in tags:
        if tag:
            if len(tag) > 25:
                tag = tag[0:25]
            if not db.query(Tag).filter(Tag.name == tag.lower()).first():
                db_tag = Tag(name=tag.lower())
                db.add(db_tag)
                db.commit()
                db.refresh(db_tag)

            if num_tags < 5:
                list_tags.append(tag.lower())
            num_tags += 1

    if num_tags >= 5:
        detail = "Only five tags can be added to an image"

    tags = db.query(Tag).filter(Tag.name.in_(list_tags)).all()

    if user.roles == Role.admin:
        image = db.query(Image).filter(Image.id == image_id).first()
    else:
        image = db.query(Image).filter(Image.id == image_id, Image.user_id == user.id).first()

    if image:
        image.updated_at = datetime.utcnow()
        image.tags = tags
        db.commit()
        db.refresh(image)
        return image, detail
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    

async def get_image(db: Session, id: int, user: User):
    """
    The get_image function is used to retrieve an image from the database.
    It takes in a database session, an id of the image to be retrieved, and a user object.
    The function returns both the image and all comments associated with that user for that particular image.

    :param db: Session: Access the database
    :param id: int: Specify the id of the image that we want to get
    :param user: User: Get the user id of the user who is logged in
    :return: The image and the comments associated with it
    """

    image = db.query(Image).filter(Image.id == id).first()

    if image:
        comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == user.id).all()
        return image, comments
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
async def get_images(db: Session, user: User):
    """
    The get_images function returns a list of images and comments for the user.
        Args:
            db (Session): The database session object.
            user (User): The current logged in user.

    :param db: Session: Access the database
    :param user: User: Get the user's comments on each image
    :return: A list of dictionaries containing the image and a list of comments
    """

    images = db.query(Image).order_by(Image.id).all()

    user_response = []
    for image in images:
        comments = db.query(Comment).filter(Comment.image_id == image.id, Comment.user_id == user.id).all()
        user_response.append({"image": image, "comments": comments})
    return user_response