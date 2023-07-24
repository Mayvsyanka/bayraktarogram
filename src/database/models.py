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
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    roles = Column('roles', Enum(Role), default=Role.user)
    comments = relationship('Comment', back_populates='author')

# class Photo(Base)
# -тут будет модель созданная другим членом команды - ее нужно замечить с коментами
# comments = relationship('Comment', back_populates='author')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String(250))
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='comments')
    #photo_id = Column(Integer, ForeignKey('photo.id'))
    #photo = relationship('Photo', back_populates='comments')