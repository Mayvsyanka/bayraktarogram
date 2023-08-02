from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import Role
from src.repository.users import get_user_by_email


async def update_user(email, role: Role, db: Session):
    """
    The update_user function updates the user's role in the database.
    
    :param email: Find the user in the database
    :type email: str
    :param role: Pass in the role object that will be assigned to the user
    :type role: Role
    :param db: Pass the database session to the function
    :type db: Session
    :return: A user object with the updated role
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.roles = role
    db.commit()
    return (user)


async def block_user(email: str, db: Session):
    """
    The block_user function takes an email address and a database connection as arguments.
    It then uses the get_user_by_email function to retrieve the user object from the database,
    and sets its access attribute to False. It then commits this change to the database, and returns a string indicating that it has done so.
    
    :param email: str: Specify the email of the user that is to be banned
    :param db: Session: Pass the database session into the function
    :return: A string message
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.access = False
    db.commit()
    return (f"User {email} is banned now")


async def unblock_user(email: str, db: Session):
    """
    The unblock_user function takes an email address and a database connection as arguments.
    It then uses the get_user_by_email function to retrieve the user object from the database,
    and sets its access attribute to True. It then commits this change to the database, and returns 
    a string indicating that it has been done.
    
    :param email: str: Get the email of the user that we want to unblock
    :param db: Session: Pass the database session to the function
    :return: A string
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.access = True
    db.commit()
    return (f"User {email} is not banned now")

