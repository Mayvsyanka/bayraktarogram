from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import access as repository_access
from src.services.auth import auth_service
from src.schemas import UserDb
from src.conf.config import settings
from src.services.roles import allowed_operation_admin
from src.schemas import Role

router = APIRouter(prefix="/access", tags=["access"])


@router.put("/block_user", dependencies=[Depends(allowed_operation_admin)])
async def unblock_user(email: str, current_user: User = Depends(auth_service.get_current_user),
                     db: Session = Depends(get_db)):
    user = await repository_access.unblock_user(email, db)
    return (user)


@router.put("/unblock_user", dependencies=[Depends(allowed_operation_admin)])
async def block_user(email: str, current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    user = await repository_access.block_user(email, db)
    return (user)


@router.put("/{contact_id}", response_model=UserDb, dependencies=[Depends(allowed_operation_admin)])
async def update_access(user_email: str, new_role:str, user: User=Depends(auth_service.get_current_user), db: Session=Depends(get_db)):

    """
    The update_access function updates the role of a user in the database.
    
    :param user_email: Identify the user that will be updated
    :type user_email: str
    :param new_role: Update the role of a user
    :type new_role: str
    :param user: Get the current user and check if they have admin access
    :type user: User
    :param db: Pass the database session to the function
    :type db: Session
    :return: A dict object
    :rtype: User
    """
    user = await repository_access.update_user(user_email, new_role, db)
    return(user)
