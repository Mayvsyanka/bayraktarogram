from sqlalchemy import Column, Integer, String, Boolean, func, Table, UniqueConstraint, Enum, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base
from src.schemas import Role
from typing import List

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(250), nullable=False, unique=True)
    bio = Column(String(500))
    location = Column(String(500))
    password = Column(String(255), nullable=False)
    crated_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    roles = Column('roles', Enum(Role), default=Role.user)
    access = Column(Boolean, default=True)
    comments = relationship('Comment', back_populates='author')
    message = relationship('Message', back_populates='user')

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    text_message = Column(String(500), unique=False)
    reciever = Column(String(50), unique=False)
    sender = Column("sender", String(
        50), ForeignKey('users.email', ondelete='CASCADE'))
    user = relationship('User', back_populates='message')

image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(300), unique=True, index=True)
    description = Column(String(500), nullable=True)
    public_name = Column(String(), unique=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="images")
    tags = relationship("Tag", secondary=image_m2m_tag, backref="images")
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())

    comments = relationship('Comment', back_populates='image')
    transformated_images_settings = relationship("ImageSettings", back_populates='image')



class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String(250))
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user_id = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'))
    author = relationship('User', back_populates='comments')
    image_id = Column('image_id', Integer, ForeignKey('images.id', ondelete='CASCADE'))
    image = relationship('Image', back_populates='comments')


class ImageSettings(Base):

    __tablename__ = 'transformated_images_settings'
    id = Column(Integer, primary_key=True)
    url = Column(String(300), unique=False, index=True)
    secure_url = Column(String(300), unique=False, index=True)
    transformed_url = Column(String(300), unique=False, index=True)
    qrcode_url = Column(String(300), unique=False, index=True)
    user_id = Column('user_id', ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    new_image_id = Column('new_image_id', ForeignKey(
        'images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="images_settings")
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    one_star = Column(Boolean, default=False)
    two_stars = Column(Boolean, default=False)
    three_stars = Column(Boolean, default=False)
    four_stars = Column(Boolean, default=False)
    five_stars = Column(Boolean, default=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="ratings")
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="ratings")

