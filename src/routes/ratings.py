from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import RatingModel, RatingResponse
from src.repository import ratings as repository_ratings
from src.services.auth import auth_service
from src.services.roles import  allowed_operation_everyone, allowed_operation_mod_and_admin

router = APIRouter(prefix='/ratings', tags=["ratings"])

@router.get("/image/{image_id}", response_model=float, dependencies=[Depends(allowed_operation_everyone)])
async def get_image_rating(image_id,
                            _: User = Depends(auth_service.get_current_user),
                              db: Session = Depends(get_db)):
    """
    The get_image_rating function returns the average rating of an image.
        The function takes in a single parameter, the image_id, and returns a JSON object containing 
        the average rating of that particular image.
    
    :param image_id: Get the average rating for a specific image
    :param _: User: Get the current user from the auth_service
    :param db: Session: Access the database
    :return: The average rating for a particular image
    """
    get_rating = await repository_ratings.get_average_rating(image_id, db)
    return get_rating


@router.get("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(allowed_operation_everyone)])
async def read_rating(rating_id: int, 
                      _: User = Depends(auth_service.get_current_user), 
                      db: Session = Depends(get_db)):
    """
    The read_rating function is used to read a rating from the database.
        The function takes in an integer representing the id of the rating and returns a RatingModel object.
    
    
    :param rating_id: int: Specify the rating_id that we want to update
    :param _: User: Make sure that the user is logged in
    :param db: Session: Get the database session
    :return: A rating object
    """
    rating = await repository_ratings.get_rating(rating_id, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    return rating

@router.post("/{image_id}", response_model=RatingResponse, dependencies=[Depends(allowed_operation_everyone)])
async def create_rate(image_id, body: RatingModel, current_user: User = Depends(auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    """
    The create_rate function creates a new rating for an image.
        The function takes in the following parameters:
            - image_id: The id of the image to be rated. This is a required parameter and must be passed in as part of the URL path.
            - body: A RatingModel object containing all information about the rating, including its score and comment (if any). This is a required parameter and must be passed in as JSON data within request body. 
    
    :param image_id: Identify the image that is being rated
    :param body: RatingModel: Specify the model that will be used to validate the request body
    :param current_user: User: Get the user information from the token
    :param db: Session: Pass the database session to the function
    :return: A rating object
    """
    rating = await repository_ratings.create_rating(image_id, body, current_user, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please verify image_id. You may not rate your images or give 2 or more ratings for 1 image")
    return rating


@router.put("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(allowed_operation_everyone)])
async def update_rating(body: RatingModel, rating_id: int, db: Session = Depends(get_db),
                        _: User = Depends(auth_service.get_current_user)):
    """
    The update_rating function updates a rating in the database.
        It takes a RatingModel object as input, and returns the updated RatingResponse object.
        If no rating is found with that id, it raises an HTTPException.
    
    :param body: RatingModel: Specify the data model that will be used to create a new rating
    :param rating_id: int: Identify the rating to be deleted
    :param db: Session: Get the database session
    :param _: User: Ensure that the user is logged in
    :return: The updated rating
    """
    rating = await repository_ratings.update_rating(rating_id, body, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Rating not found")
    return rating
    

@router.delete("/{rating_id}", response_model=RatingResponse, dependencies=[Depends(allowed_operation_mod_and_admin)])
async def remove_rating(rating_id: int, db: Session = Depends(get_db),
                        _: User = Depends(auth_service.get_current_user)):
    """
    The remove_rating function removes a rating from the database.
        It takes in an integer representing the id of the rating to be removed, and returns a RatingResponse object.
        If no such rating exists, it raises an HTTPException with status code 404.
    
    :param rating_id: int: Get the rating id from the request
    :param db: Session: Pass the database session to the repository
    :param _: User: Make sure that the user is authenticated before removing a rating
    :return: The deleted rating
    """
    rating = await repository_ratings.remove_rating(rating_id, db)
    if rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No rating found or you don't have enough rules to remove")
    return rating