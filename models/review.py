""" Review module for the HBNB project """
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, String

class Review(BaseModel, Base):
    """ Represents a Review in MySQL Database
    Inherits from BaseModel and Base (in this order)
    Attributes:
        __tablename__(str) :- Represents table name reviews
        text(sqlalchemy String) :- Represents Review description
        place_id(sqlalchemy String) :- Represents Review's place_id
        user_id(sqlalchemy String) :- Represents Owner of Review
    """
    __tablename__ = "reviews"
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    text = Column(String(1024), nullable=False)
