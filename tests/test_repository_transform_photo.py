import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from sqlalchemy.orm import Session

from src.database.models import ImageSettings, User
from src.repository.transform_photo import create_transformed_photo_url, get_transformed_qrcode, get_transformed_url


class  TestTransformPhotoRepository:
    
    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new session object and assigns it to the self.session variable, which will be used by all tests in this class.
        
        :param self: Represent the instance of the class
        :return: A magicmock object
        :doc-author: Trelent
        """
        
        self.session = MagicMock(spec=Session)
        # self.user = User(id=1)
    
    async def test_create_transformed_photo_url(self):
        """
        The test_create_transformed_photo_url function tests the create_transformed_photo_url function.
            The test is successful if the user id of the body matches that of a user in our database.
        
        :param self: Represent the instance of the class
        :return: The following error:
        :doc-author: Trelent
        """
        
        body = ImageSettings(
            user_id=1,
            image_id=1,
            trfnsformation =[
                { "radius": "max"},
                {"effect": "sepia"},
                {"width": "500"},
                {"height": "500"},
                {"crop": "fill"},
                {"gravity": "face"},
                {"color_space": "srgb" },
                {"angle": "45"}   
            ]
        )
        user_id = ImageSettings.user_id
        self.session.query().filter().all.return_value = body
        result = await create_transformed_photo_url(body=body, db=self.session, user=self.user)
        self.assertEqual(result.user_id, user_id)


    async def test_get_transformed_url(self):
        """
        The test_get_transformed_url function tests the get_transformed_url function.
            The test is successful if the transformed url is returned.
        
        :param self: Represent the instance of the class
        :return: A tuple of the id and transformed_url from the database
        :doc-author: Trelent
        """
        
        transformed_url = (ImageSettings.id, ImageSettings.transformed_url) 
        self.session.query().filter().first.return_value = transformed_url
        result = await get_transformed_url(db=self.session, id=1, user=self.user)
        self.assertEqual(result, transformed_url)

    async def test_get_transformed_qrcode(self):
        """
        The test_get_transformed_qrcode function tests the get_transformed_qrcode function.
        The test_get_transformed_qrcode function is a coroutine that takes in a database session, an id, and a user.
        The test asserts that the result of calling get transformed qrcode with these parameters is equal to the qr code url.
        
        :param self: Represent the instance of the class
        :return: The qrcode_url
        :doc-author: Trelent
        """
        
        qrcode_url = (ImageSettings.id, ImageSettings.qrcode_url)
        self.session.query().filter().first.return_value = qrcode_url
        result = await get_transformed_qrcode(db=self.session, id=1, user=self.user)
        self.assertEqual(result, qrcode_url)
        
        
        
            
            

if __name__ == '__main__':
    unittest.main()