from sqlalchemy.orm import Session
from src.database.models import User
from src.database.models import ImageSettings, Image, User
from fastapi import HTTPException, status
from src.services.photo_services import create_qrcode, createImageTag, getAssetInfo, uploadImage
import qrcode



async def get_transformated_url(db: Session, id: int, user: User):
    """
    The get_transformated_url function returns a transformated url by id
    
    :param db: Session: Access the database
    :param id: int: Get the id of the image settings that we want to update
    :param user: User: Get the user id from the user object
    :return: A transformated_url object
    :doc-author: Trelent
    """
    transformated_url = db.query(ImageSettings).filter(ImageSettings.id == id, ImageSettings.user_id == user.id).first()
    
    if not transformated_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transformated url with id {id} not found")
    else:
        return transformated_url
    

async def get_transformed_qrcode(db:Session, qrcode_url_id: int, current_user: User):
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
        qrcode_url = db.query(ImageSettings).filter(ImageSettings.id == qrcode_url_id, ImageSettings.user_id == current_user.id).first()
        
        if not qrcode_url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Qrcode url with id {qrcode_url_id} not found")
        else:
            return qrcode_url 
        
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
    public_name = result.public_name
    
    # Build the URL for the image 
    secure_url = uploadImage(image_url, public_name)
    
    # Create the transformed image url
    transformation_url = createImageTag(public_id=public_name,
                                        radius=body.radius,
                                        effect=body.effect,
                                        width=body.width,
                                        height=body.height,
                                        crop=body.crop,
                                        gravity=body.gravity,
                                        color_space=body.color_space,
                                        angle=body.angle
                                        )
    
    #create file qr_code.png with qrcode 
    create_qrcode(transformation_url)
    #qrcode's file path
    qrcode_url = "D:/cloudinary_web//bayraktarogram/qr_code.png"
    
    #add urls to body
    body.secure_url = secure_url
    body.transformed_url = transformation_url
    body.qrcode_url = qrcode_url

    #add settings to body
    image_settings = ImageSettings(**body.dict()) 
    image_settings.user_id = current_user.id
    #add settings to database
    db.add(image_settings)
    db.commit()
    db.refresh(image_settings) 
    return image_settings