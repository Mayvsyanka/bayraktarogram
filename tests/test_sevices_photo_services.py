import unittest
import uuid
import qrcode

from dotenv import load_dotenv
load_dotenv() # take environment variables from .env.

# Import the Cloudinary libraries
# ==============================
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

# from src.services.photo_services import  create_qrcode, createImageTag, getAssetInfo, uploadImage


def create_qrcode(data): # data is a string
    """
    The create_qrcode function takes a string as input and creates a QR code image file.
        Args:
            data (str): The string to be encoded in the QR code.
    
    
    :param data: Pass in the data that is to be encoded
    :return: None
    :doc-author: Trelent
    """
    
    # Data to be encoded data
    # Encoding data using make() function
    img = qrcode.make(data)
    # Saving as an image file
    file_name = 'test.png' 
    img.save(file_name)
    return file_name


def uploadImage(src_url, public_id):
    """
    The uploadImage function uploads an image to Cloudinary and returns the URL of the uploaded image.
        Args:
            src_url (str): The path to the source file on your local machine. 
            public_name (str): The name of your asset in Cloudinary's Media Library. 
        Returns:
            str: A URL pointing to a version of this asset that is stored in Cloudinary's cloud-based storage.

    :param src_url: Specify the source image to upload
    :param public_name: Set the public id of the uploaded image
    :return: The image url
    :doc-author: Trelent
    """

    # Upload the image and get its URL
    # ==============================

    # Upload the image. C:/Users/Oleg/OneDrive/GOIT_cloud/cloudinary-upload/src/images/front_face.jpg
    # Set the asset's public ID and allow overwriting the asset with new versions
    
    cloudinary.uploader.upload(src_url,
                               public_id=public_id,
                               unique_filename = False,
                               overwrite=True)
    # cloudinary.uploader.upload("https://cloudinary-devs.github.io/cld-docs-assets/assets/images/butterfly.jpeg", public_name="quickstart_butterfly", unique_filename = False, overwrite=True)
    
    
    # Build the URL for the image and save it in the variable 'srcURL'
    srcURL = cloudinary.CloudinaryImage(public_id).build_url()

    # Log the image URL to the console. 
    # Copy this URL in a browser tab to generate the image on the fly.
    print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")
    return srcURL
  
  
def getAssetInfo(public_id):
    """
    The getAssetInfo function gets and uses details of the image.
        It first gets image details and saves it in the variable 'image_info'.
        Then, it assigns tags to the uploaded image based on its width. 
        The new tag is saved in the variable 'update_resp'

    :param public_name: Identify the image
    :return: The image_info variable
    :doc-author: Trelent
    """
    # Get and use details of the image
    # ==============================

    # Get image details and save it in the variable 'image_info'.
    image_info=cloudinary.api.resource(public_id)
    print("****3. Get and use details of the image****\nUpload response:\n", json.dumps(image_info,indent=2), "\n")

# Assign tags to the uploaded image based on its width. Save the response to the update in the variable 'update_resp'.
    if image_info["width"]>900:
        update_resp=cloudinary.api.update(public_id, tags = "large")
    elif image_info["width"]>500:
        update_resp=cloudinary.api.update(public_id, tags = "medium")
    else:
        update_resp=cloudinary.api.update(public_id, tags = "small")
        
            # Log the new tag to the console.
    print("New tag: ", update_resp["tags"], "\n") 
    return image_info


def createImageTag(public_id, transformation):
    """
    The createImageTag function takes in a public_name, and returns an image tag with transformations applied to the src URL.
        Args:
            public_name (str): The name of the uploaded image file. 
            radius (int): The corner radius of the transformed image. Default is 0 pixels. 
            effect (str): A string representing one of Cloudinary's effects, such as &quot;sepia&quot;. Default is &quot;sepia&quot;.
            width (int): The width in pixels that you want your transformed image to be resized to. Default is 500px wide by 500px high if no
    
    :param public_name: Specify the name of the image to be transformed
    :param radius: Round the corners of an image
    :param effect: Apply an effect to the image
    :param width: Specify the width of the image
    :param height: Set the height of the image in pixels
    :param crop: Determine how the image is cropped
    :param gravity: Determine the position of the image
    :param color_space: Specify the color space of the image
    :param angle: Rotate the image
    :return: A url with transformations applied to the src url
    :doc-author: Trelent
    """
    
    # Transform the image
    # ==============================

    # Create an image tag with transformations applied to the src URL.
    imageTag = cloudinary.CloudinaryImage(public_id).build_url(transformation=transformation)    

    #To return only the URL, and not the whole tag, replace build_url with image
    # imageTag = cloudinary.CloudinaryImage("quickstart_butterfly").build_url(radius="max", effect="sepia")

    # Log the image tag to the console
    print("****4. Transform the image****\nTransfrmation URL: ", imageTag, "\n")
    return imageTag


class TestPhotoServices(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        The setUpClass function is called once for the class.
            It is a class method and so it receives the cls parameter that points to the class—not the object instance.
            The setUpClass function can also be used to allocate expensive resources for a test suite, such as starting up an external database.
        
        :param cls: Pass the class object
        :return: Nothing
        :doc-author: Trelent
        """
        
        print('Start before all test')

    @classmethod
    def tearDownClass(cls):
        """
        The tearDownClass function is called after all tests in the class have been run.
        It is used to clean up resources that were created during the setUpClass function.
        
        :param cls: Pass the class object to the method
        :return: The last value of the function
        :doc-author: Trelent
        """
        
        print('Start after all test')

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new instance of the class to be tested, and sets up any variables that are needed for the tests.
        
        :param self: Represent the instance of the class
        :return: Nothing
        :doc-author: Trelent
        """
        
        print('Start before each test')

    def tearDown(self):
        """
        The tearDown function is called after each test function.
            It can be used to clean up resources that were created in the setUp function.
            If you don't need to do any cleanup, you can omit this method.
        
        :param self: Represent the instance of the class
        :return: A string
        :doc-author: Trelent
        """
        
        print('Start after each test')

    
    def test_create_qrcode(self):
        """
        The test_create_qrcode function tests the create_qrcode function in the photo_services.py file.
            The function takes in one parameter:
                - url: A string representing a url that will be used to create a qrcode.
            The function returns a qrcode image.
        
        :param url: str: A string representing a url that will be used to create a qrcode.
        :return: A qrcode image.
        :doc-author: Trelent
        """
        url = "https://www.google.com"
        result = create_qrcode(url)
        print(f"result: {result}")
        self.assertEqual(result, "test.png")
        
    def test_uploadImage(self):
        """
        The test_uploadImage function tests the uploadImage function in the photo_services.py file.
            The function takes in one parameter:
                - url: A string representing a url that will be used to create a qrcode.
            The function returns a qrcode image.
        
        :param url: str: A string representing a url that will be used to create a qrcode.
        :return: A qrcode image.
        :doc-author: Trelent
        """
        url = "D:/cloudinary_web//bayraktarogram//tests/images//test_1.jpg"
        result = uploadImage(url, public_id="test_new")
        print(f"result: {result}")
        self.assertEqual(result, "http://res.cloudinary.com/doambmvei/image/upload/test_new")
        
        
    def test_getAssetInfo(self):
        """
        The test_getAssetInfo function tests the getAssetInfo function.
            The test_getAssetInfo function takes no arguments and returns nothing.
            The test_getAssetInfo function asserts that the result of calling getAssetInfo with a public id is not None.
        
        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        
        public_id = "test"  
        result = getAssetInfo(public_id)
        print(f"result: {result}")
        self.assertIsNotNone(result, None)
    
    def test_createImageTag(self):
        """
        The test_createImageTag function tests the createImageTag function.
            The test_createImageTag function takes no arguments and returns nothing.
            The test_createImageTag function asserts that the result of calling createImageTag with a public id is not None.
        
        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        
        public_id = "test"  
        result = createImageTag(public_id, transformation={"radius":"max", "effect":"sepia"})
        print(f"result: {result}")
        self.assertEqual(result, "http://res.cloudinary.com/doambmvei/image/upload/e_sepia,r_max/test")
        

# def main():
#    create_qrcode("https://www.google.com")
       
if __name__ == '__main__':
    unittest.main()

    



 