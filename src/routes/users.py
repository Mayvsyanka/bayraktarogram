"""Module for User's operations"""

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from sqlalchemy import func

from src.database.db import get_db
from src.database.models import User, Image
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import UserDb, UpdateUser, Profile
from src.conf.config import settings
from src.services.roles import allowed_operation_admin

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/me/", response_model=UserDb)
async def update_profile(body: UpdateUser, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    user = await repository_users.update_profile(body, current_user, db)
    return user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.

    
    :param file: Get the file from the request body
    :type file: UploadFile
    :param current_user: Get the current user from the database
    :type current_user: User
    :param db: Pass the database session to the repository layer
    :type db: Session
    :return: User with updated avatar
    :rtype: User
    """
    cloudinary.config(
        cloud_name=settings.cloud_name,
        api_key=settings.api_key,
        api_secret=settings.api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f'ContactsApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'ContactsApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user

@router.get("/profile/{user}", response_model=Profile)
async def get_profile(username: str, _: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    user_info = await repository_users.get_user_info(username, db)
    photos = db.query(func.count()).filter(Image.id == user_info.id).scalar()
    return {"username": user_info.username, 
            "email": user_info.email,
            "crated_at": user_info.crated_at,
            "avatar": user_info.avatar,
            "bio": user_info.bio,
            "location": user_info.location,
            "images": photos}
