from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import UserDb, AccessUserUpdate
from src.conf.config import settings
from src.services.roles import allowed_operation_admin

router = APIRouter(prefix="/users", tags=["users"])



@router.put("/{contact_id}", response_model=UserDb, dependencies=[Depends(allowed_operation_admin)])
async def update_access(user_email: str, body: AccessUserUpdate, user: User=Depends(auth_service.get_current_user), db: Session=Depends(get_db)):
    contact = await repository_users.update_user(user_email, body.email, db)
    return(contact)