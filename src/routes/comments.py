from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import CommentModel, CommentResponse
from src.repository import comments as repository_comments
from src.database.models import Comment, User, Photo
from src.services.auth import auth_service

router = APIRouter(prefix='/comments', tags=["comments"])


@router.get("/", response_model=List[CommentResponse])
async def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    comments = await repository_comments.get_comments(skip, limit, current_user, db)
    return comments


@router.get("/{comment_id}", response_model=CommentResponse)
async def read_comment(comment_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comments.get_comment(comment_id, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.post("/", response_model=CommentResponse)
async def create_comment(body: CommentModel, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    return await repository_comments.create_comment(body, current_user, db)


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(body: CommentModel, comment_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comments.update_comment(comment_id, current_user, body, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.delete("/{comment_id}", response_model=CommentResponse)
async def remove_comment(comment_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_comments.remove_comment(comment_id, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment

