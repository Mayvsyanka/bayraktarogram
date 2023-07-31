import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from sqlalchemy.orm import Session

from src.database.models import ImageSettings
from src.repository.transform_photo import create_transformed_photo_url


class  TestTransformPhotoRepository:
    
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


if __name__ == '__main__':
    unittest.main()