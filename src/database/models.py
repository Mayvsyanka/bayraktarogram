from sqlalchemy import Column, Integer, String, Boolean, func, Table, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base
from src.schemas import Role

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    roles = Column('roles', Enum(Role), default=Role.user)
    access = Column(Boolean, default=True)
    comments = relationship('Comment', back_populates='author')

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
    comments = relationship('Comment', back_populates='images')
    settings = relationship("ImageSettings", back_populates='images')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String(250))
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='comments')
    photo_id = Column(Integer, ForeignKey('images.id'))
    photo = relationship('Image', back_populates='comments')


class ImageSettings(Base):
    __tablename__ = 'transformated_images_settings'
    id = Column(Integer, primary_key=True)
    url = Column(String(300), unique=True, index=True)
    secure_url = Column(String(300), unique=True, index=True)
    transformation_url = Column(String(300), unique=True, index=True)
    angle = Column(Integer, nullable=False, default=0)
    radius = Column(Integer, nullable=False, default=0)
    effect = Column(String(50), nullable=False, default='sepia')
    width = Column(Integer, nullable=False, default=500)
    height = Column(Integer, nullable=False, default=500)
    gravity = Column(String(50), nullable=False, default='face')
    crop = Column(String(50), nullable=False, default='fill')
    color_space = Column(String(50), nullable=False, default='srgb')
    user_id = Column('user_id', ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    new_image_id = Column('new_image_id', ForeignKey(
        'images.id', ondelete='CASCADE'), default=None)
    image = relationship('Image', backref="transformated_images_settings")
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
