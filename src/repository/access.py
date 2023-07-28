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
    user = await get_user_by_email(email, db)
    user.access = False
    db.commit()
    return (f"User {email} is banned now")


async def unblock_user(email: str, db: Session):
    user = await get_user_by_email(email, db)
    user.access = True
    db.commit()
    return (f"User {email} is unbanned now")
