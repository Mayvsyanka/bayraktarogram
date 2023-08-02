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
    image = await repository_find.get_photo_by_tag(tag, db, sort_by)
    return image


@router.get("/find/words")
async def get_photo_by_key_words(words: str, _: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db), sort_by: SortField = Query(SortField.date, description="Sort by field (date or rating)")):
    image = await repository_find.get_photo_by_key_words(words, db, sort_by)
    return image
