from typing import Optional, List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.database.models import Comment, User, Image, Role
from src.schemas import CommentModel, CommentUpdateModel, CommentResponse

async def get_comment(comment_id: int, db: Session) -> Optional[CommentResponse]:
    """
    Retrieves a single comment with the specified ID.

    :param comment_id: The ID of the comment to retrieve.
    :param db: The database session.
    :return: The comment with the specified ID, or None if it does not exist.
    """
    comment_res = db.query(Comment).filter(Comment.id == comment_id).first()
    print("Comment Result:", comment_res)
    if comment_res:
        return CommentResponse(content=comment_res.content, id=comment_res.id)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

async def update_comment(body: CommentUpdateModel, user: User, db: Session) -> Optional[CommentResponse]:
    """
    Updates a single comment with the specified ID created by the specific user.

    :param note_id: The ID of the comment to update.
    :param body: The updated data for the comment.
    :param user: The user that created the current comment.
    :param db: The database session.
    :return: The updated comment, or None if it does not exist.
    """
    comment = db.query(Comment).filter(Comment.id == body.id).first()

    if comment:
        if user.id == comment.user_id:
            comment.content = body.content
            db.commit()
            return CommentResponse(content=comment.content, id=comment.id)

    return None


async def get_comments(photo_id: int, db: Session)-> List[CommentResponse]:
    """
    Retrieves a list of comments for a specific photo with specified pagination parameters.

    :param photo_id: The photo id to retrieve comments for.
    :type photo_id: int
    :param db: The database session.
    :type db: Session
    :return: A list of comments.
    :rtype: List[Comment]
    """
    all_comments=[]

    image = db.query(Image).filter(Image.id == photo_id).first()

    if image:
        comments_list = db.query(Comment).filter(Comment.image_id == photo_id).all()
        for comment in comments_list:
            all_comments.append(CommentResponse(content=comment.content, id=comment.id))
        return all_comments
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


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


async def remove_comment(comment_id: int, user: User, db: Session) -> Optional[CommentResponse]:
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
    if user.roles == Role.admin or user.roles == Role.moderator:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if comment:
            db.delete(comment)
            db.commit()
            return CommentResponse(content=comment.content, id=comment.id)

        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")



