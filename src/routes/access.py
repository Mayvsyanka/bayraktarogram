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


@router.put("/unblock_user/{email}", dependencies=[Depends(allowed_operation_admin)])
async def unblock_user(email: str, current_user: User = Depends(auth_service.get_current_user),
                     db: Session = Depends(get_db)):
    """
    The unblock_user function unblocks a user by email.
        Args:
            email (str): The email of the user to be unblocked.
            current_user (User): The currently logged in user, who is performing the action.
            db (Session): A database session object for interacting with the database.
    
    :param email: str: Specify the email of the user to be unblocked
    :param current_user: User: Get the current user
    :param db: Session: Access the database
    :return: The user object that was unblocked
    :doc-author: Trelent
    """
    user = await repository_access.unblock_user(email, db)
    return (user)


@router.put("/block_user", dependencies=[Depends(allowed_operation_admin)])
async def block_user(email: str, current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    """
    The block_user function blocks a user from the database.
        Args:
            email (str): The email of the user to be blocked.
            current_user (User): The currently logged in user, who is blocking another user.
            db (Session): A database session object for interacting with the database.
    
    :param email: str: Get the email of the user to be blocked
    :param current_user: User: Get the user who is currently logged in
    :param db: Session: Access the database
    :return: A user object
    :doc-author: Trelent
    """
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
