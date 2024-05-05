#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """ Represents a User in MySQL Database
    Inherits from BaseModel and Base (in this order)
    Attributes:
        __tablename__(str) :- Represents table name users
        email(sqlalchemy String) :- Represents User email Address
        password(sqlalchmey String) :- Represents User password
        first_name(sqlalchemy String) :- Represents User first name
        last_name(sqlalchemy String) :- Represents User last name
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", backref="user", cascade="delete")
    reviews = relationship("Review", backref="user", cascade="delete")
