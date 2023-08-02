from fastapi import APIRouter, Depends, status, UploadFile, File, Query
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from sqlalchemy import func
from enum import Enum

from src.repository import find as repository_find
from src.database.db import get_db
from src.database.models import User, Image
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import UserDb, UpdateUser, Profile, SortField
from src.conf.config import settings
from src.services.roles import allowed_operation_admin
from typing import Optional

router = APIRouter(prefix="/find", tags=["find"])



@router.get("/find/tag")
async def get_photo_by_tag(tag: str, _: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db), sort_by: SortField = Query(SortField.date, description="Sort by field (date or rating)")):
    """
    The get_photo_by_tag function returns a list of photos that have the specified tag.
        The function takes in a string representing the tag and an optional sort_by parameter, which defaults to SortField.date if not provided.
    
    :param tag: str: Specify the tag that we want to search for
    :param _: User: Get the current user, but it is not used in the function
    :param db: Session: Pass the database session to the function
    :param sort_by: SortField: Sort the images by date or rating
    :param description: Provide a description for the parameter
    :return: A list of photos that have a particular tag
    :doc-author: Trelent
    """
    image = await repository_find.get_photo_by_tag(tag, db, sort_by)
    return image


@router.get("/find/words")
async def get_photo_by_key_words(words: str, _: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db), sort_by: SortField = Query(SortField.date, description="Sort by field (date or rating)")):
    """
    The get_photo_by_key_words function returns a list of photos that match the key words provided by the user.
        The function takes in two parameters:
            -words: A string containing one or more key words separated by spaces.
            -sort_by: An enum value indicating how to sort the results (date or rating).
    
    :param words: str: Search for the photo by keywords
    :param _: User: Get the current user
    :param db: Session: Get the database session from the dependency injection container
    :param sort_by: SortField: Sort the results by date or rating
    :param description: Describe the parameter in the swagger documentation
    :return: The image that has the words in its title or description
    :doc-author: Trelent
    """
    image = await repository_find.get_photo_by_key_words(words, db, sort_by)
    return image
