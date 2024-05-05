#!/usr/bin/env python3
"""place Module"""
from os import getenv
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, Integer, Float
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import Table


#if getenv("HBNB_TYPE_STORAGE", None) == "db":
association_table = Table("place_amenity", Base.metadata,
                        Column("place_id", String(60),
                                ForeignKey("places.id"),
                                primary_key=True, nullable=False),
                        Column("amenity_id", String(60),
                                ForeignKey("amenities.id"),
                                primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """Represents a Place for MySQL database
    Inherits from BaseModel and Base (in this order)
    Attributes:-
        __tablename__(str): Represents Table name Places
        city_id(sqlalchemy String): Represents city id, fkey to cities.id
        user_id(sqlalchemy String): Represents user id, fkey to users.id
        name(sqlalchemy String): Represents city name
        description(sqlalchemy String): Represents city description
        number_rooms(sqlalchemy Integer): Represents number of rooms
        number_bathrooms(sqlalchemy Integer): Represents number of bathrooms
        max_guest(sqlalchemy Integer): Represents number of maximum guests
        price_by_night(sqlalchemy Integer): Represents price by night
        Latitude(sqlalchemy Float): Represents Latitude
        Longitude(sqlalchemy Float): Represents Longitude
    fkey -- Foriegn key    
    """

    #if getenv("HBNB_TYPE_STORAGE", None) == "db":
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float) 
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary=association_table,
                            viewonly=False, overlaps="place_amenities")
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Get a list of all linked Reviews."""
            review_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Get/set linked Amenities."""
            amenity_list = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
