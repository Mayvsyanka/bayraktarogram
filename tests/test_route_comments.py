from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app

from src.services.auth import auth_service


client = TestClient(app)

def test_create_comment(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/comments/add",
            json={'content': "test_comment", 'image_id': 3},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["content"] == "test_comment"


def test_get_comment(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/comments_by_id/1",
            json={'content': "test_comment", 'id': 1},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["content"] == "test_comment"


def test_get_comment_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/comments_by_id/20",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["content"] == "Comment not found"


def test_get_comments(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/comments_to_photo/{photo_id}",
            json={'content': "test_comment", 'image_id': 1},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["content"] == "test_comment"


def test_update_comment(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/comments/update/1",
            json={'content': "test_comment", 'id': 1},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["content"] == "new_test_comment"


def test_update_comment_not_found(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/comments/update/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["content"] == "Comment not found"


def test_delete_comment(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/comments/delete/1",
            json={'content': "test_comment", 'id': 1},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["content"] == "deleted"

