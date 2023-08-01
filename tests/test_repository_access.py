import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import User
from src.repository.users import get_user_by_email
from src.schemas import Role
from src.repository.access import update_user


@pytest.fixture
def db_session():

    return MagicMock(spec=Session)


def test_update_user(db_session):

    email = "test@example.com"
    role = Role.admin
    user = User(id=1, email=email, roles=Role.user)
    db_session.query().filter().first.return_value = user


    async def async_db_session():
        return db_session


    updated_user = update_user(email, role, async_db_session)


    assert updated_user.id == 1
    assert updated_user.email == email
    assert updated_user.roles == role

    db_session.query().filter().first.assert_called_once_with()

    db_session.commit.assert_called_once()
