import unittest
from unittest.mock import MagicMock

from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.database.models import Image, User, Tag, Comment
from src.routes.images import add_image
from src.schemas import  ImageAddTagModel, Role
from src.repository.images import normalize_tags
from src.routes import images

class TestImagesRoute(unittest.TestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new database session and adds some sample data to it.

        :param self: Represent the instance of the class
        :return: A mock session object, a mock admin user,
        """

        self.db = MagicMock(spec=Session)
        self.admin_user = User(id=1, roles=Role.admin)
        self.non_admin_user = User(id=2, roles=Role.user)
        self.image1 = Image(id=1, user_id=1)
        self.image2 = Image(id=2, user_id=2)
        self.comment1 = Comment(id=1, user_id=1, image_id=1)
        self.comment2 = Comment(id=2, user_id=2, image_id=2)
        self.tag1 = Tag(id=1, name='tag1')
        self.tag2 = Tag(id=2, name='tag2')
        self.current_user = User(id=1, username='testuser')
        self.body = MagicMock()
        self.file = UploadFile(filename='test.jpg', file=MagicMock())

    async def test_get_image_as_admin(self):
        """
        The test_get_image_as_admin function tests the get_image function in images.py
            The test_get_image_as_admin function is a coroutine that takes three arguments: self, db, and admin user.
            The test case uses MagicMock to mock the database query filter first method to return image 1 from the database. 
            It also mocks the all method of query filter to return comment 1 from the database. 
                Then it calls await on images get image with an id of one and passes in mocked db and admin user as arguments.
        
        :param self: Represent the instance of the class
        :return: The image, the number of comments and a list of comments
        """
   
        self.db.query.return_value.filter.return_value.first.return_value = self.image1
        self.db.query.return_value.filter.return_value.all.return_value = [self.comment1]

        result = await images.get_image(1, self.db, self.admin_user)
        self.assertEqual(result, (self.image1, 5, [self.comment1]))

    async def test_get_image_as_user(self):
        """
        The test_get_image_as_user function tests the get_image function in images.py
            The test_get_image_as_user function is a coroutine that takes three arguments: self, db, and non-admin user.
            The test uses MagicMock to mock the database query filter first and all functions. 
            It then calls the get image function with an image id of 2 (which corresponds to self.image2) and passes it 
                a mocked database object as well as a non-admin user object (self.non-admin). 

        :param self: Access the attributes and methods of the class in python
        :return: The image2 object, the number of likes for that image (4), and a list with only one comment in it
        """

        self.db.query.return_value.filter.return_value.first.return_value = self.image2
        self.db.query.return_value.filter.return_value.all.return_value = [self.comment2]

        result = await images.get_image(2, self.db, self.non_admin_user)

        self.assertEqual(result, (self.image2, 4, [self.comment2]))

    async def test_add_image(self):
        """
        The test_add_image function tests the add_image function.
        It mocks the normalize_tags and images functions, and then calls add_image with a body, file, db, current user.
        The test asserts that result['image'] is equal to expected image (which was returned by images mock), 
        and that result['detail'] is equal to 'Image was successfully added.' + details (which were returned by images mock). 
        Then it asserts that normalize tags was called once with self.body as an argument; change name was called once with 'test' and self.db as arguments; 
        and finally it

        :param self: Represent the instance of the class
        :return: A dictionary with two keys: image and detail
        """

        normalize_tags_mock = MagicMock(return_value=['tag1', 'tag2', 'tag3'])
        change_name_mock = MagicMock(return_value='correct_name')
        normalize_tags = normalize_tags_mock
        images_service_change_name = change_name_mock

        expected_image = MagicMock()

        images_mock = MagicMock()
        images_mock.add_image.return_value = (expected_image, 'details')

        with unittest.mock.patch('app.main.images', images_mock):
            result = await add_image(self.body, self.file, self.db, self.current_user)

        self.assertEqual(result['image'], expected_image)
        self.assertEqual(result['detail'], 'Image was successfully added.details')

        normalize_tags_mock.assert_called_once_with(self.body)
        change_name_mock.assert_called_once_with('test', self.db)
        images_mock.add_image.assert_called_once_with(self.db, self.body, ['tag1', 'tag2', 'tag3'],
                                                      'src_url', 'correct_name', self.current_user)
        
    async def test_add_tag(self):
        """
        The test_add_tag function tests the add_tag function in images.py.
        The test_add_tag function is a unit test that checks if the add tag functionality works as intended.
        It does this by mocking out all of the functions and classes that are called within the add tag functionality, 
        and then checking to see if they were called correctly.

        :param self: Represent the instance of the class
        :return: The image object
        """

        self.db.query.return_value.filter.return_value.first.return_value = self.image1
        self.db.query.return_value.filter.return_value.all.return_value = [self.tag1, self.tag2]
        self.db.commit.return_value = None
        self.db.refresh.return_value = None

        image_add_tag_model = ImageAddTagModel(tags=['tag1', 'tag2'])

        result = await images.add_tag(1, image_add_tag_model, self.db, self.admin_user)

        self.assertEqual(result, self.image1)
        self.db.query.return_value.filter.assert_called_with(Tag.name.in_(['tag1', 'tag2']))
        self.db.query.return_value.filter.assert_called_with(Image.id == 1)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_with(self.image1)

    async def test_delete_image(self):
        """
        The test_delete_image function tests the delete_image function in images.py.
        It creates a mock database and image, then calls the delete_image function with an id of 1 and admin user credentials.
        The test asserts that the result is equal to self.image 1, which was created earlier in this file as a MagicMock object.

        :param self: Access the attributes and methods of the class in python
        :return: The image that was deleted
        """

        self.db.query.return_value.filter.return_value.first.return_value = self.image1
        self.db.delete.return_value = None
        self.db.commit.return_value = None

        result = await images.delete_image(1, self.db, self.admin_user)

        self.assertEqual(result, self.image1)
        self.db.query.return_value.filter.assert_called_with(Image.id == 1)
        self.db.delete.assert_called_with(self.image1)
        self.db.commit.assert_called_once()





