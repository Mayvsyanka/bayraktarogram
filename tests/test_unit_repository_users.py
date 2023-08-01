import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
    update_profile,
    get_user_info,
)
from src.schemas import UserModel
from src.database.models import User


class TestUserModule(unittest.TestCase):

    def setUp(self):

        self.db_session = MagicMock(spec=Session)

    def test_get_user_by_email(self):

        self.db_session.query().filter().first.return_value = User(
            id=1, email="test@example.com", avatar=None)
        user = get_user_by_email("test@example.com", self.db_session)
        self.assertEqual(user.email, "test@example.com")

    def test_create_user(self):

        user_data = UserModel(email="new_user@example.com",
                              password="password123", bio="Hello, I'm a new user")
        self.db_session.query().first.return_value = None
        new_user = create_user(user_data, self.db_session)
        self.assertEqual(new_user.email, "new_user@example.com")

    def test_update_token(self):

        user = User(id=1, email="test@example.com", avatar=None)
        update_token(user, "new_refresh_token", self.db_session)
        self.assertEqual(user.refresh_token, "new_refresh_token")

    def test_confirmed_email(self):

        self.db_session.query().filter().first.return_value = User(
            id=1, email="test@example.com", avatar=None)
        confirmed_email("test@example.com", self.db_session)
        self.assertTrue(self.db_session.commit.called)

    def test_update_avatar(self):

        self.db_session.query().filter().first.return_value = User(
            id=1, email="test@example.com", avatar=None)
        user = update_avatar("test@example.com",
                             "https://example.com/avatar.jpg", self.db_session)
        self.assertEqual(user.avatar, "https://example.com/avatar.jpg")

    def test_update_profile(self):

        user = User(id=1, email="test@example.com", avatar=None)
        profile_data = UserModel(bio="Hello, I'm updated", location="New York")
        updated_user = update_profile(profile_data, user, self.db_session)
        self.assertEqual(updated_user.bio, "Hello, I'm updated")
        self.assertEqual(updated_user.location, "New York")

    def test_get_user_info(self):

        self.db_session.query().filter().first.return_value = User(
            id=1, email="test@example.com", avatar=None)
        user_info = get_user_info("test@example.com", self.db_session)
        self.assertEqual(user_info.email, "test@example.com")


if __name__ == '__main__':
    unittest.main()
