from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import TagModel, TagResponse
from src.repository import tags as repository_tags
from src.services.auth import auth_service
from src.services.roles import allowed_operation_mod_and_admin, allowed_operation_everyone


router = APIRouter(prefix='/tags', tags=["tags"])


@router.post("/", response_model=TagResponse, dependencies=[Depends(allowed_operation_everyone)])
async def create_tag(body: TagModel, db: Session = Depends(get_db), 
                    _: User = Depends(auth_service.get_current_user)):
    """
    The create_tag function creates a new tag in the database.
        It takes a TagModel object as input and returns the created tag.


    :param body: TagModel: Pass the data from the request body
    :param db: Session: Pass the database connection to the function
    :param _: User: Check if the user is logged in
    :return: A tagmodel object
    """

    check_tag = await repository_tags.get_tags(body.name.lower(), db)
    if check_tag:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Tag already exist')
    tag = await repository_tags.create_tag(body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Verification error')
    return tag

@router.get("/", response_model=List[TagResponse], dependencies=[Depends(allowed_operation_everyone)])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
                    _: User = Depends(auth_service.get_current_user)):
    """
    The read_tags function returns a list of tags.
    
    :param skip: int: Skip the first n tags
    :param limit: int: Limit the number of tags returned
    :param db: Session: Pass the database session to the repository layer
    :param _: User: Make sure that the user is authenticated
    :return: A list of tag objects
    """
    
    tags = await repository_tags.get_tags(skip, limit, db)
    return tags

@router.get("/{tag_id}", response_model=TagResponse, dependencies=[Depends(allowed_operation_everyone)])
async def read_tag(tag_id: int, db: Session = Depends(get_db),
                   _: User = Depends(auth_service.get_current_user)):
    """
    The read_tag function returns a tag by its id.
    
    :param tag_id: int: Specify the tag id to be updated
    :param db: Session: Pass the database session to the repository layer
    :param _: User: Ensure that the user is authenticated
    :return: A tag object, which is a dictionary
    """
    
    tag = await repository_tags.get_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag

@router.put("/{tag_id}", response_model=TagResponse, dependencies=[Depends(allowed_operation_mod_and_admin)])
async def update_tag(body: TagModel, tag_id: int, db: Session = Depends(get_db), 
                     _: User = Depends(auth_service.get_current_user)):
    """
    The update_tag function updates a tag in the database.
        It takes a TagModel object as input, and returns the updated tag.
        If no such tag exists, it raises an HTTPException with status code 404.
    
    :param body: TagModel: Pass the tagmodel object to the function
    :param tag_id: int: Specify the id of the tag to be deleted
    :param db: Session: Get the database session
    :param _: User: Check if the user is authenticated
    :return: A tagmodel object
    """
    
    tag = await repository_tags.update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag

@router.delete("/{tag_id}", response_model=TagResponse, dependencies=[Depends(allowed_operation_mod_and_admin)]) 
async def delete_tag(tag_id: int, db: Session = Depends(get_db), 
                     _: User = Depends(auth_service.get_current_user)):
    """
    The delete_tag function deletes a tag from the database.
        It takes in an integer representing the id of the tag to be deleted, and returns a TagResponse object containing information about that tag.
    
    
    :param tag_id: int: Specify the id of the tag to be deleted
    :param db: Session: Get the database session
    :param _: User: Make sure that the user is logged in
    :return: A tag object, which is the same as a post object
    """
    
    tag = await repository_tags.delete_tag_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag
    


