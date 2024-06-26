#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv


Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs['updated_at'],
                        '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.updated_at = datetime.utcnow()

            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs['created_at'],
                        '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get('__class__', None):
                del kwargs['__class__']
            self.__dict__.update(kwargs)
            self.id = str(uuid.uuid4())

    def __str__(self):
        """Returns a string representation of the instance"""
        dictionary = {}
        dictionary.update(self.__dict__)
        if dictionary.get('_sa_instance_state', None):
            del dictionary['_sa_instance_state']
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, dictionary)

    def save(self):
        from models import storage
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        #self.__dict__.pop('_sa_instance_state', None)
        dictionary.update(self.__dict__)
        if dictionary.get('_sa_instance_state', None):
            del dictionary['_sa_instance_state']
        dictionary.update({'__class__':
            (str(type(self)).split('.')[-1]).split('\'')[0]})
        #print(type(dictionary['created_at'].isoformat()))
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        from models import storage
        """deletes the current instance from the storage (models.storage)
        when called"""
        storage.delete(self)
