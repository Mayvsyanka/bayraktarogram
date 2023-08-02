from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from src.database.models import User, Message


async def send_message (receiver, sender, message, db:Session):
    """
    The send_message function takes in a receiver, sender, message and db.
    It then creates a new Message object with the text_message being the message passed in.
    The reciever is set to be the receiver passed in and sender is set to be the email of 
    the user who sent it (sender). The function then adds this new Message object to our database 
    and commits it so that we can refresh it later on. Finally, we return this newly created message.
    
    :param receiver: Specify the email of the user that will receive the message
    :param sender: Get the sender's email address
    :param message: Pass the message to be sent
    :param db:Session: Pass the database session to the function
    :return: The message object
    :doc-author: Trelent
    """
    message = Message(text_message=message,
                      reciever=receiver, sender=sender.email)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

async def read_messages (user, db:Session):
    """
    The read_messages function takes a user and a database session as arguments.
    It returns all messages in the database that were sent to or from the given user.
    
    :param user: Determine which messages to return
    :param db:Session: Access the database
    :return: All messages that the user has sent or recieved
    :doc-author: Trelent
    """
    return db.query(Message).filter(or_(Message.sender == user.email, Message.reciever == user.email)).all()

async def delete_messages (message_id, user, db:Session):
    """
    The delete_messages function deletes a message from the database.
        Args:
            message_id (int): The id of the message to be deleted.
            user (User): The user who is deleting the message.
    
    :param message_id: Find the message in the database
    :param user: Check if the user is the reciever of a message
    :param db:Session: Pass in the database session
    :return: A message, which is a string
    :doc-author: Trelent
    """
    message = db.query(Message).filter(and_(Message.id == message_id, user.email == Message.reciever)).first()
    if message:
        db.delete(message)
        db.commit()
    else:
        message = f"Message with id: {message_id} does not exist"
    return message
