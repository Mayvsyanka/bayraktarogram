from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime

import pytest

from src.database.models import User, Image
from src.repository.ratings import get_image
from src.services.auth import auth_service

RATING = {
           "one_star": False,
            "two_stars": True,
            "three_stars": False,
            "four_stars": False,
            "five_stars": False}

UPDATED_RATING = {
           "one_star": False,
            "two_stars": False,
            "three_stars": True,
            "four_stars": False,
            "five_stars": False}

#@pytest.fixture()
#def token(client, user, session, monkeypatch):
#    mock_send_email = MagicMock()
#    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
#    client.post("/api/auth/signup", json=user)
#   current_user: User = session.query(User).filter(User.email == user.get('email')).first()
#    current_user.confirmed = True
#    session.commit()
#    response = client.post(
#        "/api/auth/login",
#        data={"username": user.get('email'), "password": user.get('password')},
#    )
#    data = response.json()
#   return data["access_token"]


def test_create_rating(client, token):
    fake_image = Image(url="test_url", 
                       description="test_description", 
                       public_name="test_name", 
                       user_id=2, 
                       created_at=datetime(year=2020, month=2, day=20), 
                       updated_at=datetime(year=2020, month=2, day=20))
    with patch("src.repository.ratings.get_image", return_value=fake_image):
        response = client.post("api/ratings/1", json=RATING, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        rating = response.json()
        assert rating["one_star"] == RATING["one_star"]


def test_get_ratings(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/ratings/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["one_star"] == RATING["one_star"]


def test_get_rating_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/ratings/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Rating not found"


def test_get_image_rating(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/ratings/image/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text

def test_update_rating(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/ratings/1",
            json=UPDATED_RATING,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["one_star"] == RATING["one_star"]


def test_delete_tag(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/ratings/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["one_star"] == RATING["one_star"]