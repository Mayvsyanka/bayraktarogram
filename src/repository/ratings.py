from sqlalchemy.orm import Session

from src.database.models import Rating, User, Image
from src.schemas import RatingModel
from fastapi import HTTPException


async def get_average_rating(image_id, db: Session):
    """
    The get_average_rating function takes in an image_id and a database session.
    It then queries the Rating table for all ratings associated with that image_id.
    If there are no ratings, it returns 0 as the average rating. If there are ratings, 
    it sums up all of the star values (one star = 1 point, two stars = 2 points etc.) 
    and divides by the number of total ratings to get an average rating.

    :param image_id: Find the ratings for a specific image
    :param db: Session: Pass the database session to the function
    :return: The average rating of a given image
    """
    image_ratings = db.query(Rating).filter(Rating.image_id == image_id).all()
    if len(image_ratings) == 0:
        return 0
    sum_user_rating = 0
    for el in image_ratings:
        if el.one_star:
            sum_user_rating += 1
        if el.two_stars:
            sum_user_rating += 2
        if el.three_stars:
            sum_user_rating += 3
        if el.four_stars:
            sum_user_rating += 4
        if el.five_stars:
            sum_user_rating += 5
    average_user_rating = sum_user_rating / len(image_ratings)

    return average_user_rating

async def get_rating(rating_id: int, db: Session) -> Rating:
    """
    The get_rating function takes in a rating_id and a database session.
    It then queries the database for the rating with that id, and returns it.

    :param rating_id: int: Specify the id of the rating we want to get
    :param db: Session: Pass in the database session
    :return: The rating object for the given id
    """
    return db.query(Rating).filter(Rating.id == rating_id).first()

def get_image(db: Session, image_id: int):
    """
    The get_image function takes a database session and an image id as parameters.
    It then queries the database for the image with that id, and returns it if found.
    If not found, it raises an HTTPException.

    :param db: Session: Access the database
    :param image_id: int: Find the image in the database
    :return: A single image from the database
    """
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

async def create_rating(image_id: int, body: RatingModel, user: User, db: Session) -> Rating:
    """
    The create_rating function takes in an image_id, a RatingModel object, and a user.
    It then checks if the image exists in the database. If it does not exist, it returns None.
    If the image does exist but is owned by the user who is trying to rate it, 
    it also returns None because you cannot rate your own images. It then checks that only one of 
    the five rating options has been selected (i.e., that sum_of_rates == 1). If this condition is not met, 
    it also returns None because you can only select one rating option per picture.

    :param image_id: int: Get the image from the database
    :param body: RatingModel: Get the rating from the user
    :param user: User: Get the user id of the current user
    :param db: Session: Access the database
    :return: A rating object
    """
    image_in_database = get_image(db, image_id)

    if image_in_database.user_id == user.id:
        return None
    sum_of_rates = 0

    for el in body:
        if el[1]:
            sum_of_rates += 1

    if sum_of_rates != 1:
        return None
    rating_in_database = db.query(Rating).filter(Rating.image_id == image_id, 
                                                 Rating.user_id == user.id).first()

    if rating_in_database:
        return rating_in_database
    
    rating = Rating(one_star=body.one_star, 
                    two_stars=body.two_stars, 
                    three_stars=body.three_stars,
                    four_stars=body.four_stars, 
                    five_stars=body.five_stars, 
                    user_id=user.id, 
                    image_id=image_id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating

async def update_rating(rating_id: int, body: RatingModel, db: Session):
    """
    The update_rating function takes in a rating_id and a body of type RatingModel.
    It then checks to see if the sum of all the rates is greater than 1, if it is, it returns None.
    If not, it queries for the rating with that id and updates its values to those in body.

    :param rating_id: int: Find the rating in the database
    :param body: RatingModel: Pass the data from the request to the function
    :param db: Session: Access the database
    :return: The updated rating
    """
    sum_of_rates = 0
    for el in body:
        if el[1]:
            sum_of_rates += 1
    if sum_of_rates > 1:
        return None
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        rating.one_star = body.one_star
        rating.two_stars = body.two_stars
        rating.three_stars = body.three_stars
        rating.four_stars = body.four_stars
        rating.five_stars = body.five_stars
        db.commit()
    return rating

async def remove_rating(rating_id: int, db: Session):
    """
    The remove_rating function removes a rating from the database.
        Args:
            rating_id (int): The id of the rating to be removed.
            db (Session): A connection to the database.

    :param rating_id: int: Identify the rating to be removed
    :param db: Session: Pass the database session to the function
    :return: The rating that is deleted
    """
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        db.delete(rating)
        db.commit()
    return rating