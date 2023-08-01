import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Image, Comment
from src.schemas import CommentModel
from src.repository.comments import (
    get_comment,
    update_comment,
    get_comments,
    create_comment,
    remove_comment,
)

from tests.conftest.py import engine, db


class TestComment(unittest.IsolatedAsyncioTestCase):

    def test_get_comment_not_found(db):
        comment_id = 123456  # Assuming there's no comment with this ID
        with pytest.raises(Exception) as exc_info:
            get_comment(comment_id, db)
        assert exc_info.type == HTTPException
        assert exc_info.value.status_code == 404

    def test_get_comment_found(db):
        # Assuming there's a comment with ID 1 in the database
        comment_id = 1
        comment_res = get_comment(comment_id, db)
        assert comment_res is not None
        assert comment_res.id == comment_id

    def test_update_comment_not_found(db):
        body = {"id": 123456, "content": "new_test_comment"}
        user = User(id=1, roles=Role.user)  # Assuming the user exists and is not an admin or moderator
        updated_comment = update_comment(body, user, db)
        assert updated_comment is None

    def test_update_comment_found(db):
        # Assuming there's a comment with ID 1 in the database, and the user with ID 1 is its creator
        body = {"id": 1, "content": "new_test_comment"}
        user = User(id=1, roles=Role.user)
        updated_comment = update_comment(body, user, db)
        assert updated_comment is not None
        assert updated_comment.content == "new_test_comment"

    def test_get_comments_not_found(db):
        photo_id = 123456  # Assuming there's no image with this ID
        with pytest.raises(Exception) as exc_info:
            get_comments(photo_id, db)
        assert exc_info.type == HTTPException
        assert exc_info.value.status_code == 404

    def test_get_comments_found(db):
        # Assuming there's an image with ID 1 and it has comments in the database
        photo_id = 1
        comments_list = get_comments(photo_id, db)
        assert isinstance(comments_list, List)

    def test_create_comment(db):
        # Assuming there's a user with ID 1 and an image with ID 3 in the database
        body = {"content": "test_comment", "image_id": 3}
        user = User(id=1, roles=Role.user)
        new_comment = create_comment(body, user, db)
        assert new_comment is not None
        assert new_comment.content == "test_comment"

    def test_remove_comment_not_found(db):
        comment_id = 123456  # Assuming there's no comment with this ID
        user = User(id=1, roles=Role.user)  # Assuming the user exists and is not an admin or moderator
        removed_comment = remove_comment(comment_id, user, db)
        assert removed_comment is None

    def test_remove_comment_found(db):
        # Assuming there's a comment with ID 1 in the database, and the user with ID 1 is an admin or moderator
        comment_id = 1
        user = User(id=1, roles=Role.admin)  # Assuming the user is an admin or moderator
        removed_comment = remove_comment(comment_id, user, db)
        assert removed_comment is not None

if __name__ == '__main__':
    unittest.main()