from typing import List

from sqlalchemy.orm import Session

from sqlalchemy import and_

from src.database.models import Comment, User, Photo
from src.schemas import CommentModel


async def get_comments(skip: int, limit: int,  photo: Photo, db: Session) -> List[Comment]:
    """
    Retrieves a list of comments for a specific photo with specified pagination parameters.

    :param skip: The number of notes to skip.
    :type skip: int
    :param limit: The maximum number of notes to return.
    :type limit: int
    :param photo: The photo to retrieve comments for.
    :type photo: Photo
    :param db: The database session.
    :type db: Session
    :return: A list of comments.
    :rtype: List[Comment]
    """
    return db.query(Comment).filter(Comment.photo_id == photo.id).offset(skip).limit(limit).all()


async def get_comment(comment_id: int, db: Session) -> Comment:
    """
    Retrieves a single comment with the specified ID.

    :param comment_id: The ID of the comment to retrieve.
    :type comment_id: int
    :param db: The database session.
    :type db: Session
    :return: The comment with the specified ID, or None if it does not exist.
    :rtype: Comment | None
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


async def create_comment(body: CommentModel, user: User, photo: Photo, db: Session) -> Comment:
    """
    Creates a new comment for a specific photo.

    :param body: The data for the comment to create.
    :type body: CommentModel
    :param user: Current user that created current comment.
    :type user: User
    :param photo: The photo to retrieve comments for.
    :type photo: Photo
    :param db: The database session.
    :type db: Session
    :return: The newly created comment.
    :rtype: Comment
    """
    comment = Comment(content = body.content, user_id = user.id, photo_id = photo.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def update_comment(comment_id: int, body: CommentModel, user: User, db: Session) -> Comment | None:
    """
    Updates a single comment with the specified ID created by the specific user.

    :param note_id: The ID of the comment to update.
    :type note_id: int
    :param body: The updated data for the comment.
    :type body: CommentModel
    :param user: The user that created current comment.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated comment, or None if it does not exist.
    :rtype: Comment | None
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        comment.content = body.content
        db.commit()
    return comment


async def remove_comment(comment_id: int, user: User, db: Session)  -> Comment | None:
    """
    Removes a single comment with the specified ID. Can be removed only by admin or moderator.

    :param comment_id: The ID of the comment to remove.
    :type comment_id: int
    :param user: Current user that tries to remove the comment.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed comment, or None if it does not exist.
    :rtype: Comment | None
    """

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment
