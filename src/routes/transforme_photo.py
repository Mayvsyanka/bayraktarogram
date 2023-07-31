

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas import ImageSettingsModel, ImageSettingsResponseModel
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import ImageSettings, User


router = APIRouter(prefix='/transform_photo', tags=["transform_photo"])


@router.get('/transformation/{transformed_id}', response_model=List[ImageSettingsResponseModel]) 
async def get_transformared_photos(user_id: int, transformed_id: str, db: Session = Depends(get_db)):
    

    user = db.query(User).filter(User.id == user_id).first()
    url = db.query(ImageSettings).filter(ImageSettings.transformated_url.transformed_id == transformed_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    elif not transformed_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transformed photo with id {transformed_id} not found")     
    
    return url.transformed_url


@router.post('/', response_model=ImageSettingsResponseModel, status_code=status.HTTP_201_CREATED)
async def create_transformed_photo(body:ImageSettingsModel, db: Session = Depends(get_db), uploadImage=uploadImage,  createImageTag=createImageTag, create_qrcode=create_qrcode):
    user = db.query(User).filter(User.id == body.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {body.user_id} not found")
    
    
    image_settings = ImageSettings(**body.dict()) 
    
    delivery_url = uploadImage(image_settings.url, image_settings.public_name)
    transformed_url = createImageTag(image_settings.public_name)
    transformed_url_qrcode = create_qrcode(transformed_url)
    
    image_settings.secure_url = delivery_url
    image_settings.transformated_url = transformed_url
    image_settings.transformated_url_qrcode = transformed_url_qrcode
    
    
    db.add(image_settings)
    db.commit()
    db.refresh(image_settings) 
    
    return image_settings   
