from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import CommentModel, CommentResponse, CommentUpdateModel
from src.repository import comments as repository_comments
from src.database.models import Comment, User, Image
from src.services.auth import auth_service
from src.services.roles import allowed_operation_mod_and_admin, allowed_operation_everyone

router = APIRouter(prefix='/comments', tags=["comments"])


@router.get("/{photo_id}", response_model=List[CommentResponse], dependencies=[Depends(allowed_operation_everyone)])
async def get_comments(photo_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
       Retrieves a list of comments for a specific photo with specified pagination parameters.

       :param photo_id: The photo id to retrieve comments for.
       :param db: The database session.
       :return: A list of comments.
       """
    image = db.query(Image).filter(Image.id == photo_id).first()
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    comments = await repository_comments.get_comments(photo_id, db)
    return comments


@router.get("/{comment_id}", response_model=List[CommentResponse], dependencies=[Depends(allowed_operation_everyone)])
async def get_comment(comment_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
     Retrieves a single comment with the specified ID.

     :param comment_id: The ID of the comment to retrieve.
     :param db: The database session.
     :return: The comment with the specified ID, or None if it does not exist.
     """
    comment = await repository_comments.get_comment(comment_id, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.post("/add", response_model=CommentResponse, dependencies=[Depends(allowed_operation_everyone)])
async def create_comment(body: CommentModel, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    Creates a new comment for a specific photo.

    :param body: The data for the comment to create.
    :param user: Current user that created current comment.
    :param photo: The photo to retrieve comments for.
    :param db: The database session.
    :return: The newly created comment.
    """
    return await repository_comments.create_comment(body, current_user, db)


@router.put("/update/{comment_id}", response_model=CommentResponse, dependencies=[Depends(allowed_operation_everyone)])
async def update_comment(body: CommentUpdateModel, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    Updates a single comment with the specified ID created by the specific user.

    :param note_id: The ID of the comment to update.
    :param body: The updated data for the comment.
    :param user: The user that created current comment.
    :param db: The database session.
    :return: The updated comment, or None if it does not exist.
    """
    comment = await repository_comments.update_comment(body, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.delete("/delete/{comment_id}", response_model=CommentResponse, dependencies=[Depends(allowed_operation_mod_and_admin)])
async def remove_comment(comment_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    """
    Removes a single comment with the specified ID. Can be removed only by admin or moderator.

    :param comment_id: The ID of the comment to remove.
    :param user: Current user that tries to remove the comment.
    :param db: The database session.
    :return: The removed comment, or None if it does not exist.
    """
    comment = await repository_comments.remove_comment(comment_id, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


