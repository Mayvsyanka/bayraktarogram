from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.database.models import Comment, User, Image
from src.schemas import CommentModel, CommentUpdateModel


async def get_comments(photo_id: int, db: Session):
    """
    Retrieves a list of comments for a specific photo with specified pagination parameters.

    :param photo_id: The photo id to retrieve comments for.
    :type photo_id: int
    :param db: The database session.
    :type db: Session
    :return: A list of comments.
    :rtype: List[Comment]
    """
    image = db.query(Image).filter(Image.id == photo_id).first()

    if image:
        comments_list = db.query(Comment).filter(Comment.image_id==photo_id).all()
        return comments_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


async def get_comment(comment_id: int, db: Session) -> Comment | None:
    """
    Retrieves a single comment with the specified ID.

    :param comment_id: The ID of the comment to retrieve.
    :type comment_id: int
    :param db: The database session.
    :type db: Session
    :return: The comment with the specified ID, or None if it does not exist.
    :rtype: Comment | None
    """

    comment_res = db.query(Comment).filter(Comment.id == comment_id).first()

    return comment_res


async def create_comment(body: CommentModel, user: User, db: Session) -> Comment:
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
    comment = Comment(content = body.content, user_id = user.id, image_id = body.image_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def update_comment(body: CommentUpdateModel, user: User, db: Session) -> Comment | None:
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
    comment = db.query(Comment).filter(Comment.id == body.id).first()
    if comment:
        if user.id == comment.user_id:
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
    if user.roles == 'admin' or user.roles == 'moderator':
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if comment:
            db.delete(comment)
            db.commit()
        return comment


