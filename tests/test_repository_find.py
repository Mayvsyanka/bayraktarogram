from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import pytest
import asyncio

from src.repository.ratings import get_average_rating
from src.database.models import Base, User, Image, Tag, Rating
from src.schemas import SortField
from src.repository.find import get_photo_by_tag, get_photo_by_key_words

DATABASE_URL = "sqlite:///test.db"


@pytest.fixture
def db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.mark.asyncio
async def test_get_photo_by_tag(db: Session):
    tag_name = "test_tag"
    tag = Tag(name=tag_name)
    image1 = Image(description="Test Image 1")
    image2 = Image(description="Test Image 2")
    image3 = Image(description="Test Image 3")
    image1.tags.append(tag)
    image2.tags.append(tag)
    image3.tags.append(tag)
    db.add(tag)
    db.add(image1)
    db.add(image2)
    db.add(image3)
    db.commit()


    sorted_images = await get_photo_by_tag(tag_name, db, SortField.date)
    assert len(sorted_images) == 3
    assert sorted_images[0].created_at <= sorted_images[1].created_at

    sorted_images = await get_photo_by_tag(tag_name, db, SortField.rating)
    assert len(sorted_images) == 3


@pytest.mark.asyncio
async def test_get_photo_by_key_words(db: Session):
    image1 = Image(description="Test Image 1")
    image2 = Image(description="Test Image 2")
    image3 = Image(description="Another Image")
    db.add(image1)
    db.add(image2)
    db.add(image3)
    db.commit()

    sorted_images = await get_photo_by_key_words("Test", db, SortField.date)
    assert len(sorted_images) == 2
    assert sorted_images[0].created_at <= sorted_images[1].created_at

    sorted_images = await get_photo_by_key_words("Test", db, SortField.rating)
    assert len(sorted_images) == 2


@pytest.mark.asyncio
async def test_get_average_rating(db: Session):
    image = Image(description="Test Image")
    rating1 = Rating(rating=4)
    rating2 = Rating(rating=5)
    image.ratings.append(rating1)
    image.ratings.append(rating2)
    db.add(image)
    db.commit()

    average_rating = await get_average_rating(image.id, db)
    assert average_rating == pytest.approx((4 + 5) / 2.0, 0.01)


