import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Photo, Comment
from src.schemas import CommentModel
from src.repository.comments import (
    get_comments,
    get_comment,
    create_comment,
    remove_comment,
    update_comment,
)


class TestComment(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, roles='admin')
        self.photo = Photo(id=1)

    async def test_get_comments(self):
        comments = [Comment(), Comment(), Comment()]
        self.session.query().filter().offset().limit().all.return_value = comments
        result = await get_comments(skip=0, limit=10, photo=self.photo, db=self.session)
        self.assertEqual(result, comments)

    async def test_get_comment_found(self):
        comment = Comment()
        self.session.query().filter().first.return_value = comment
        result = await get_comment(comment_id=1, db=self.session)
        self.assertEqual(result, comment)

    async def test_get_comment_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_comment(comment_id=1, db=self.session)
        self.assertIsNone(result)

    async def test_create_comment(self):
        body = CommentModel(content="test comment", user_id=self.user.id, user_roles=self.user.roles,
                            photo_id=self.photo.id)
        self.session.query().filter().all.return_value = comment
        result = await create_comment(body=body, user=self.user, photo=self.photo, db=self.session)
        self.assertEqual(result.content, body.content)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_comment_found(self):
        comment = Comment()
        self.session.query().filter().first.return_value = comment
        result = await remove_comment(comment_id=1, user=self.user, db=self.session)
        self.assertEqual(result, comment)

    async def test_remove_comment_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_comment(comment_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_comment_found(self):
        body = CommentModel(content="test comment", user_id=self.user.id, user_roles=self.user.roles,
                            photo_id=self.photo.id)
        self.session.query().filter().all.return_value = comment
        self.session.query().filter().first.return_value = comment
        self.session.commit.return_value = None
        result = await update_comment(comment_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, comment)

    async def test_update_comment_not_found(self):
        body = CommentModel(content="test comment", user_id=self.user.id, user_roles=self.user.roles,
                            photo_id=self.photo.id)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_comment(comment_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
