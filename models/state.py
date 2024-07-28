#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
import shlex


class State(BaseModel, Base):
    """ State class
    Attributes:
        name: state name.
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan', backref="state")

    if models.storage_t != 'db':
        @property
        def cities(self):
            """Return the list of City objects from storage linked to the current State."""
            obj_dict = models.storage.all(City)
            return [city for city in obj_dict.values() if city.state_id == self.id]
