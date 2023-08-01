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
    message = await repository_message.send_message(reciever, sender, message, db)
    return(message)


@router.get("/read_message/")
async def read_messages(user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    messages = await repository_message.read_messages(user, db)
    return (messages)

@router.delete("/delete_message/{message_id}")
async def delete_message(message_id, user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    message = await repository_message.delete_messages(message_id, user, db)
    return(message)
