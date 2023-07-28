import unittest
from datetime import datetime
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Image, User, Tag, Comment
from src.repository.images import delete_image, add_tag, update_image, add_image,  get_image, get_images, normalize_tags
from src.schemas import ImageUpdateModel, ImageAddModel, Role

class TestImagesService(unittest.TestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new database session and adds some sample data to it.
        
        :param self: Represent the instance of the class
        :return: The object of the class
        :doc-author: Trelent
        """
        self.db = MagicMock(spec=Session)
        self.user = User(id=1, roles=Role.user)
        self.image = MagicMock()
        self.tags = ['tag1', 'tag2']
        self.url = 'https://test.jpg'
        self.public_name = 'Test Image'
        self.user_id = 1
        self.image_id = 1
        self.description = "some text for test"

    async def test_get_images(self):
        """
        The test_get_images function tests the get_images function.
        The test_get_images function is a unit test for the get_images function.
        It checks that when given a database and user, it returns an array of images with comments.

        :param self: Refer to the current instance of a class
        :return: The following
        """

        self.db.query.return_value.order_by.return_value.all.return_value = [
            Image(id=1, description='Test Image 1', user_id=1),
            Image(id=2, description='Test Image 2', user_id=2)
        ]

        expected_response = [
            {
                'image': Image(id=1, description='Test Image 1', user_id=1),
                'comments': [Comment(id=1, user_id=1, image_id=1, content='Nice image')]
            }
        ]

        result = await get_images(self.db, self.user)
        self.assertEqual(result, expected_response)

    async def test_get_image(self):
        """
        The test_get_image function tests the get_image function.
        The test_get_image function is a unit test for the get_image function.
        It checks that when given an image id, it returns the correct image object and its rating and comments.

        :param self: Refer to the instance of the class
        :return: A tuple containing the image, the average rating and a list of comments
        """

        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, description='Test Image 1',
                                                                                  user_id=1)

        expected_result = (
            Image(id=1, description='Test Image 1', user_id=1),
            4.2,
            [Comment(id=1, user_id=1, image_id=1, content='Nice image')]
        )

        result = await get_image(self.db, 1, self.user)
        self.assertEqual(result, expected_result)

    async def test_add_image(self):
        """
        The test_add_image function tests the add_image function.
        The test_add_image function is a unit test for the add_image function.
        It tests that when given an ImageAddModel, two tags, and a url, description and user object it returns an image object with id 1.

        :param self: Access the attributes and methods of the class in python
        :return: A tuple of the image and a list of tags
        """

        self.db.query.return_value.filter.return_value.first.return_value = User(id=1)

        self.db.add.return_value = None
        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        expected_image = Image(id=1, description='Test Image', user_id=1)

        result = await add_image(self.db, ImageAddModel(description='Test Image'), ['tag1', 'tag2'], 'https://test.jpg',
                                 'Test Image', self.user)
        self.assertEqual(result[0], expected_image)

    async def test_update_image(self):
        """
        The test_update_image function tests the update_image function.
        The test_update_image function is a unit test for the update_image function.
        It checks that when an image is updated, it returns the new image with its new description.
        
        :param self: Refer to the current instance of a class
        :return: The expected image
        """
       
        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, description='Old Description',
                                                                                  user_id=1)

        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        expected_image = Image(id=1, description='New Description', user_id=1)

        result = await update_image(self.db, 1, ImageUpdateModel(description='New Description'), self.user)
        self.assertEqual(result, expected_image)

    async def test_add_tag(self):
        """
        The test_add_tag function tests the add_tag function.
        The test_add_tag function is a unit test for the add_tag function.
        It checks that when given valid input, it returns an image object with tags and no error message.

        :param self: Access the class attributes and methods
        :return: The expected_image, an empty string and the number of times that commit() and refresh() are called
        """

        tags_mock = ['tag1', 'tag2', 'tag3']
        normalize_tags_mock = MagicMock(return_value=tags_mock)
        normalize_tags = normalize_tags_mock

        self.db.query.return_value.filter.return_value.first.return_value = None

        self.user.roles = Role.admin

        expected_tags = [Tag(name=tag.lower()) for tag in tags_mock]
        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, user_id=1)

        expected_image = Image(id=1, user_id=1, updated_at=datetime.utcnow(), tags=expected_tags)

        result = await add_tag(self.db, self.image_id, self.body, self.user)

        self.assertEqual(result[0], expected_image)
        self.assertEqual(result[1], "")
        self.assertEqual(self.db.commit.call_count, 1)
        self.assertEqual(self.db.refresh.call_count, 1)

        normalize_tags_mock.assert_called_once_with(self.body)

    async def test_delete_image(self):
        """
        The test_delete_image function tests the delete_image function.
        It does this by creating a mock database, and then mocking the query method of that database. 
        The filter method is also mocked, as well as first(). The return value of first() is set to an Image object with id= 1 and user_id = 1. 
        The delete() and commit() methods are also mocked, with their return values being set to None. An expected image object is created using these same parameters (id= 1 and user_id = 1). 
        Then we call the actual function we want to test (delete_image) on our mock
        
        :param self: Access the attributes and methods of the class in python
        :return: The expected image
        """
    
        self.db.query.return_value.filter.return_value.first.return_value = Image(id=1, user_id=1)

 
        self.db.delete.return_value = None
        self.db.commit.return_value = None

        expected_image = Image(id=1, user_id=1)

        result = await delete_image(self.db, 1, self.user)
        self.assertEqual(result, expected_image)



