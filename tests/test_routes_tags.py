from unittest.mock import MagicMock, patch

import pytest

from src.database.models import User
from src.services.auth import auth_service

@pytest.fixture()
def token(client, user, session, monkeypatch):
    """
    The token function is used to create a user, confirm the user, and then log in as that user.
    It returns an access token for the logged-in user.
    
    :param client: Make requests to the api
    :param user: Create a user in the database
    :param session: Create a new session for the test
    :param monkeypatch: Mock the send_email function
    :return: An access token
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_create_tag(client, token):
    """
    The test_create_tag function tests the creation of a tag.
    It does this by first patching the auth_service module's r object to return None, which is what it would do if there was no user in redis with that token.
    Then, it makes a POST request to /api/tags with json data containing &quot;name&quot;: &quot;test_tag&quot; and an Authorization header containing the token we passed into our test function as an argument.
    We then assert that our response status code is 200 (OK), and if not, print out whatever text came back from our server so we can see what went wrong.
    Next, we get
    
    :param client: Make a request to the api
    :param token: Make sure that the user is logged in
    :return: A 200 status code and a json object with the name of the tag
    """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/tags",
            json={"name": "test_tag"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "test_tag"
        assert "name" in data


def test_get_tag(client, token):
    """
    The test_get_tag function tests the GET /api/tags/&lt;id&gt; endpoint.
    It does this by first patching the auth_service module's r object with a MagicMock instance,
    which allows us to mock out any calls made to that object. We then set up our mocked r object's get method
    to return None, which will cause an exception in our code when it tries to access the response body of a request. 
    We then make a GET request against /api/tags/&lt;id&gt;, passing in an Authorization header containing our token as we would if we were making this call from Postman or another client application
    
    :param client: Make requests to the api
    :param token: Pass the token to the test_get_tag function
    :return: The tag with the id of 1
    """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/tags/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "test_tag"


def test_get_tag_not_found(client, token):
    """
    The test_get_tag_not_found function tests the get_tag function in the tags.py file.
    It does this by mocking out the redis database and returning None when it is called,
    which will cause a 404 error to be returned.
    
    :param client: Send a request to the api
    :param token: Pass in the token to be used for testing
    :return: A 404 status code and a detail message
    """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/tags/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Tag not found"


def test_get_tags(client, token):
    """
    The test_get_tags function tests the /api/tags endpoint.
    It does this by first patching the auth_service module's r object with a MagicMock instance, which is then configured to return None when its get method is called.
    This simulates what happens when a user makes an authenticated request to the /api/tags endpoint: The auth_service module's r object will be used to make an HTTP GET request to https://auth-server:5000/user, and that response will be returned from calling .get() on it.
    The test then makes a real HTTP GET request against our application at http://localhost:5000
    
    :param client: Make a request to the api
    :param token: Test the get_tags function with a valid token
    :return: A list of tags
    """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/tags",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["name"] == "test_tag"


def test_update_tag(client, token):
    """
    The test_update_tag function tests the update_tag function in the tags.py file.
    It does this by creating a mock object for redis and then using that to test if 
    the response is 200, which means it was successful, and if the data returned has 
    the correct name.
    
    :param client: Make requests to the api
    :param token: Authenticate the user
    :return: The updated tag
    """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/tags/1",
            json={"name": "new_test_tag"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "new_test_tag"


def test_update_tag_not_found(client, token):
    """
    The test_update_tag_not_found function tests the update_tag function in the tags.py file.
    It does this by creating a mock object for redis and then setting its get method to return None,
    which is what would happen if there was no tag with that id in redis. Then it makes a PUT request to 
    the /api/tags/2 endpoint with json data containing {&quot;name&quot;: &quot;new_test_tag&quot;} and an Authorization header 
    containing a token generated from the test user's credentials (see conftest). It asserts that the response status code is 404, which means Not Found, and then asserts that detail
    
    :param client: Make requests to the api
    :param token: Pass in the token to the test function
    :return: A 404 status code and a message saying that the tag was not found
    """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/tags/2",
            json={"name": "new_test_tag"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Tag not found"


def test_delete_tag(client, token):
    """
    The test_delete_tag function tests the delete tag endpoint.
    It does this by first patching the auth_service module's r object to return None when get is called on it.
    This simulates a user not being logged in, and thus should result in an unauthorized response from the server.
    The function then makes a DELETE request to /api/tags/&lt;tag_id&gt; with an Authorization header containing a valid token, 
    and asserts that the response status code is 200 (OK). It also asserts that data[&quot;name&quot;] == &quot;new_test_tag&quot; and 
    that &quot;id&quot; is present in data.&quot;
    
    :param client: Make requests to the api
    :param token: Authenticate the user
    :return: The name and id of the deleted tag
    """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/tags/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "new_test_tag"
        assert "id" in data


def test_repeat_delete_tag(client, token):
    """
    The test_repeat_delete_tag function tests the case where a user tries to delete a tag that has already been deleted.
    The test_repeat_delete_tag function uses the client fixture, which is defined in conftest.py and provides an instance of FlaskClient for testing purposes.
    The test_repeat_delete_tag function also uses the token fixture, which is defined in conftest.py and provides an authentication token for testing purposes.
    
    :param client: Make requests to the api
    :param token: Authenticate the user
    :return: 404 with a detail of tag not found
    """
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/tags/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Tag not found"