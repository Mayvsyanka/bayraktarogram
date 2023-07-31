

from typing import List
import os

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

import cloudinary
from cloudinary import uploader


from src.schemas import ImageSettingsModel, ImageSettingsResponseModel
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import ImageSettings, User
from src.services.auth import auth_service
from src.services.roles import allowed_operation_everyone
from src.repository import transform_photo
from src.repository.transform_photo import get_transformed_url, create_transformed_photo_url, get_transformed_qrcode
from src.conf.config import settings

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

router = APIRouter(prefix='/transform_photo', tags=["transform_photo"])


@router.post('/transformations/add', response_model=ImageSettingsResponseModel, status_code=status.HTTP_201_CREATED, dependencies=[Depends(allowed_operation_everyone)])
async def create_transformed_photo_url(body:ImageSettingsModel, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_transformed_photo_url function creates a transformed photo url.
        The function takes in an ImageSettingsModel object and returns the transformed photo url.
    
    
    :param body:ImageSettingsModel: Pass the imagesettingsmodel object to the function
    :param db: Session: Access the database
    :param current_user: User: Get the current user's id
    :return: A string
    :doc-author: Trelent
    """   
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        secure=True
    )
    return await transform_photo.create_transformed_photo_url(body, db, current_user) #await
    

@router.get('/transformations/{id}', response_model=ImageSettingsResponseModel, dependencies=[Depends(allowed_operation_everyone)])  #dependencies=[Depends(allowed_operation_everyone)
async def get_transformed_photos(id: int, db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
   
    """
    The get_transformed_photos function returns the transformed_url of a photo that has been uploaded to the database.
        The function takes in an integer, transformed_url_id, and uses it to query the database for a matching id. 
        If no match is found, then an error message is returned.
    
    :param transformed_url_id: int: Specify the transformed_url_id of the photo that is being requested
    :param db: Session: Access the database
    :param current_user: User: Get the current user
    :return: The transformed_url value
    :doc-author: Trelent
    """    
    # config = cloudinary.config(secure=True) 
    # cloudinary.config(
    #     cloud_name=os.environ.get('CLOUDINARY_NAME'),
    #     api_key=os.environ.get('CLOUDINARY_API_KEY'),
    #     api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    #     secure=True
    # )
    
    transformed_url = await get_transformed_url(db, id,  current_user)
    return {"transformed_url_id": transformed_url.id, "transformed_url": transformed_url.transformed_url}


@router.get('/transformations/{qrcode_url_id}', response_model=ImageSettingsResponseModel, dependencies=[Depends(get_db)]) 
async def get_transformed_qrcode(qrcode_url_id: int, db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_transformed_qrcode function returns the transformed qrcode_url of a given qrcode_url id.
            The function takes in an integer representing the id of a given qrcode_url and returns a dictionary containing 
            the transformed url for that particular image.
    
    :param qrcode_url_id: int: Identify the qrcode_url in the database
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user's id
    :return: The transformed qrcode_url of a given qrcode_url id
    :doc-author: Trelent
    """
    """
    The get_transformed_qrcode function returns the transformed qrcode_url of a given qrcode_url id.
        The function takes in an integer representing the id of a given qrcode_url and returns a dictionary containing 
        the transformed url for that particular image.
    
    :param qrcode_url_id: int: Identify the qrcode_url in the database
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user's id
    :return: The following error:
    :doc-author: Trelent
    """
    qrcode_url = await transform_photo.get_transformed_qrcode(db, qrcode_url_id, current_user)     
    return {"qrcode_url_id": qrcode_url}



    
    
    
  
