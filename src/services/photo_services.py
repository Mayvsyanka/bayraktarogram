# Set your Cloudinary credentials
# ==============================
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
# Import to generate a QR code

import qrcode
import uuid

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(secure=True)

# Log the configuration
# ==============================
print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")


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
       

# Create qrcode
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
    file_name = str(uuid.uuid4()) + '.png' 
    img.save(file_name)
    return file_name
       

# Create qrcode
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
    file_name = str(uuid.uuid4()) + '.png' 
    img.save(file_name)
    return file_name