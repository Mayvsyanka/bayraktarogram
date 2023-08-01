import os
from dotenv import load_dotenv, find_dotenv

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User, Image
from src.services.auth import auth_service
from src.services.roles import  allowed_operation_everyone
from src.repository import images
from src.repository.images import normalize_tags
from src.schemas import ImageAddResponse, ImageUpdateModel, ImageAddModel, ImageAddTagResponse, ImageAddTagModel, ImageGetResponse, ImageDeleteResponse, ImageUpdateDescrResponse, ImageGetAllResponse

load_dotenv(find_dotenv())

router = APIRouter(prefix='/images', tags=["images"])

@router.get("/image_id/{id}", response_model=ImageGetResponse, dependencies=[Depends(allowed_operation_everyone)])
async def get_image(id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_image function returns a JSON object containing the image and comments.
    The image is returned as an ImageAddResponse object, which contains the following fields:
        id (int): The ID of the image in our database.
        name (str): The name of the user who uploaded this image.
        url (str): A URL to access this image on Cloudinary's servers. This URL will be valid for 24 hours after it was generated, so if you want to use it later than that, you'll need to generate a new one using get_image_url(). 
        tags ([str]): A list of
    
    :param id: int: Specify the id of the image to be retrieved
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user's information
    :return: A dictionary with the image and comments
    """
    
    user_image, comments, ratings = await images.get_image(db, id, current_user)

    return {"image": user_image, "comments": comments, "ratings": ratings}


@router.put("/update_description/{image_id}", response_model=ImageUpdateDescrResponse, 
            dependencies=[Depends(allowed_operation_everyone)])
async def update_description(image_id: int, image_info: ImageUpdateModel, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_description function updates the description of an image.
        Args:
            image_id (int): The id of the image to be updated.
            image_info (ImageUpdateModel): A model containing information about how to update the description.
    
    :param image_id: int: Identify the image to be updated
    :param image_info: ImageUpdateModel: Get the image_id and description
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: A dictionary with the id, description and detail of the image
    """
    
    user_image = await images.update_image(db, image_id, image_info, current_user)
    return {"id": user_image.id, "description": user_image.description, "detail": "Image was successfully updated"}


@router.put("/update_tags/{image_id}", response_model=ImageAddTagResponse, dependencies=[Depends(allowed_operation_everyone)])
async def add_tag(image_id, body: ImageAddTagModel = Depends(), db: Session = Depends(get_db),
                  current_user: User = Depends(auth_service.get_current_user)):
    """
    The add_tag function adds a tag to an image.
        The function takes in the following parameters:
            - image_id: The id of the image that is being tagged.
            - body: A JSON object containing information about the tag being added, including its name and color. 
                    This parameter is optional; if it's not provided, then a default value will be used instead. 
    
    :param image_id: Identify the image to be updated
    :param body: ImageAddTagModel: Get the tag from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: The image id, the tags and a detail message
    """
    
    image, details = await images.add_tag(db, image_id, body, current_user)
    return {"id": image.id, "tags": image.tags, "detail": "Image was successfully updated." + details}


@router.delete("/{id}", response_model=ImageDeleteResponse, dependencies=[Depends(allowed_operation_everyone)])
async def delete_image(id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The delete_image function deletes an image from the database.
        The function takes in a user_id and an image_id, and returns a dictionary with the deleted image's information.
    
    
    :param id: int: Specify the id of the image to be deleted
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user from the auth_service
    :return: A dictionary with a key of image and a value of the deleted image
    """
    
    user_image = await images.delete_image(db, id, current_user)
    return {"image": user_image, "detail": "Image was successfully deleted"}


@router.post("/add", response_model=ImageAddResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_operation_everyone)])
async def add_image(body: ImageAddModel = Depends(), file: UploadFile = File(), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The add_image function takes a body, file, db, and current_user as parameters.
    It then calls the change_name function to make sure that the image's public name is unique.
    Then it uploads the image to Cloudinary using its API key and secret key from .env file. 
    After uploading it gets a URL for an image of size 250x250 pixels with fill crop mode from Cloudinary. 
    Finally it calls add_image function in images module which adds an Image object into database.
    
    :param body: ImageAddModel: Get the image information from the request body
    :param file: UploadFile: Upload the image to cloudinary
    :param db: Session: Access the database
    :param current_user: User: Get the user who is currently logged in
    :return: A dictionary with the image and a detail string
    """
    
    async def change_name(public_name, db):
        """
        The change_name function takes a public_name and a db as parameters.
        It then checks if the public_name is already in use by another image,
        and if it is, it adds an underscore and a number to the end of the name.
        If that name is also taken, it increments the number until there are no more images with that name.

        :param public_name: Check if the name is already taken
        :param db: Access the database
        :return: A string that is the name of the image
        """

        right_public_name = public_name
        suffix = 1

        while db.query(Image).filter(Image.public_name == right_public_name).first():
            suffix += 1
            right_public_name = f"{public_name}_{suffix}"

        return right_public_name
    
    cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
            secure=True
        )
    right_tags = await normalize_tags(body)
    public_name = file.filename.split(".")[0]
    right_public_name = await change_name(public_name, db)
    file_name = right_public_name + "_" + str(current_user.username)
    r = cloudinary.uploader.upload(file.file, 
                                   public_id=f'bayraktarogram/{file_name}',
                                   overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'bayraktarogram/{file_name}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    image, details = await images.add_image(db, body, right_tags, src_url, right_public_name, current_user)

    return {"image": image, "detail": "Image was successfully added." + details}


@router.get("", response_model=ImageGetAllResponse, dependencies=[Depends(allowed_operation_everyone)])
async def get_images(db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_images function returns a list of images that the current user has uploaded.
    The function takes in two parameters: db and current_user. The db parameter is used to 
    access the database, while the current_user parameter is used to access information about 
    the currently logged-in user.
    
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A list of images
    """
    user_images = await images.get_images(db, current_user)
    return {"images": user_images}
