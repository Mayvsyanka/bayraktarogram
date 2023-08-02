from sqlalchemy.orm import Session
from src.database.models import User
from src.database.models import ImageSettings, Image, User
from fastapi import HTTPException, status
from src.services.photo_services import create_qrcode, createImageTag, getAssetInfo, uploadImage
import qrcode
import os




async def get_transformed_url(db: Session, id: int, user: User):
    """

    The get_transformed_url function returns the transformed url of an image with a given id.
        The function takes in two parameters:
            - db: A database session object that allows us to query the database for information.
            - id: An integer representing the unique identifier of an image in our database.
        The function returns a string containing the transformed url of an image with a given id.
    
    :param db: Session: Access the database
    :param id: int: Get the id of the image settings object
    :param user: User: Get the user id and check if the image belongs to that user
    :return: A string, but the schema expects a transformedurl object
    :doc-author: Trelent
    """
    
    transformed_url = db.query(ImageSettings).filter(ImageSettings.id == id).first()
        
    if transformed_url:
        return  transformed_url.id, transformed_url.transformed_url
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transformated url with id {id} not found")
    


async def get_transformed_qrcode(db:Session, id: int, user: User):
        """
        The get_transformed_qrcode function returns a transformed qrcode image based on the user's input.
            The function takes in two parameters:
                - db: A database session object that allows us to query the database
                - qrcode_url_id: An integer representing the id of an ImageSettings object in our database
                - current_user: A User object representing who is currently logged into our application
        
        :param db:Session: Access the database
        :param qrcode_url_id: int: Get the qrcode url from the database
        :param current_user: User: Get the user id from the database
        :return: A single row from the database
        :doc-author: Trelent
        """
        qrcode_url = db.query(ImageSettings).filter(ImageSettings.id == id).first()
        
               
        if qrcode_url:
            return qrcode_url.id, qrcode_url.qrcode_url 
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Qrcode of the url with id {id} not found")
        
        
async def create_transformed_photo_url(body:ImageSettings, db: Session, current_user: User):
    """
    The create_transformed_photo_url function creates a transformed photo url and adds it to the database.
        Args:
            body (ImageSettings): The image settings that will be used to create the transformed photo url.
            db (Session): The database session object.
            current_user (User): The user who is currently logged in and making this request. 
        Returns: 
            ImageSettings: An ImageSettings object containing all of the information about an image, including its secure URL, transformation URL, QR code URL, etc.


    :param body:ImageSettings: Get the image_id, radius, effect, width and height parameters from the request body
    :param db: Session: Access the database
    :param current_user: User: Get the user_id of the current user
    :return: The image_settings object
    :doc-author: Trelent
    """

    
    # Get the image url from the database (table Image)
    result = db.query(Image).filter(Image.id == body.image_id, Image.user_id == current_user.id).first()

    image_url = result.url
    print(f'image_url from Image:', image_url)
    public_name = result.public_name
    print(f'public_name from Image:', public_name)

    if public_name is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Image with id {body.image_id} not found")
    else:
        # Build the URL for the image
        secure_url = uploadImage(image_url, public_name)
        # Get the image info
        getAssetInfo(public_name)

        # Create the transformed image url
        transformation_url = createImageTag(
            public_name, transformation=body.transformation)
        print(f'transformation_url:', transformation_url)

        folder_name = "bayraktarogram"

# Получаем текущую директорию (текущую папку)
        current_directory = os.getcwd()

# Объединяем текущую директорию с именем папки для получения полного пути
        folder_path = os.path.join(current_directory, folder_name)

# Получаем абсолютный путь к папке
        absolute_folder_path = os.path.abspath(folder_path).split("\\")

        absolute_folder_path.pop()

        path = ("\\").join(absolute_folder_path)
        # create file qr_code.png with qrcode
        qrcode_file_name = create_qrcode(transformation_url)
        # qrcode's file path
        qrcode_url = path + "\\" + qrcode_file_name
        # Create the transformed image urls
        transformatiom_image = ImageSettings(url=image_url,
                                             transformed_url=transformation_url,
                                             qrcode_url=qrcode_url,
                                             secure_url=secure_url,
                                             user_id=current_user.id)
        # Add the transformed image urls to the database
        db.add(transformatiom_image)
        db.commit()
        db.refresh(transformatiom_image)
        return transformatiom_image