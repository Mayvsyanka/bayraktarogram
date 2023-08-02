from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.services.auth import auth_service
from src.schemas import UserDb
from src.conf.config import settings
from src.services.roles import allowed_operation_admin
from src.schemas import Role
from src.repository import message as repository_message

router = APIRouter(prefix="/message", tags=["message"])

@router.put("/write_message/{reciever}")
async def write_message(reciever: str, message: str, sender: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The write_message function takes in a reciever, message, and sender.
    The function then sends the message to the reciever using the send_message function from repository_message.py
    
    :param reciever: str: Specify the user that will recieve the message
    :param message: str: Get the message from the user
    :param sender: User: Get the current user
    :param db: Session: Get the database session
    :return: The message object, which is a dict
    :doc-author: Trelent
    """
    message = await repository_message.send_message(reciever, sender, message, db)
    return(message)


@router.get("/read_message/")
async def read_messages(user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The read_messages function returns a list of messages that the user has received.
        The function takes in a User object and Session object as parameters, which are used to query the database for all messages sent to the user.
        The function returns a list of Message objects.
    
    :param user: User: Get the current user, and db: session is used to connect to the database
    :param db: Session: Pass the database session to the function
    :return: A list of messages
    :doc-author: Trelent
    """
    messages = await repository_message.read_messages(user, db)
    return (messages)

@router.delete("/delete_message/{message_id}")
async def delete_message(message_id, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The delete_message function deletes a message from the database.
        
    
    :param message_id: Specify which message to delete
    :param user: User: Get the current user
    :param db: Session: Pass the database session to the function
    :return: A message object
    :doc-author: Trelent
    """
    message = await repository_message.delete_messages(message_id, user, db)
    return(message)
