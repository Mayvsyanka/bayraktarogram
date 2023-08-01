from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from src.database.models import User, Message


async def send_message (receiver, sender, message, db:Session):
    message = Message(text_message=message,
                      reciever=receiver, sender=sender.email)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

async def read_messages (user, db:Session):
    return db.query(Message).filter(or_(Message.sender == user.email, Message.reciever == user.email)).all()

async def delete_messages (message_id, user, db:Session):
    message = db.query(Message).filter(and_(Message.id == message_id, user.email == Message.reciever)).first()
    if message:
        db.delete(message)
        db.commit()
    else:
        message = f"Message with id: {message_id} does not exist"
    return message
