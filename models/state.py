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
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        """return the list of City objects from storage linked to the
        current State."""
        obj = models.storage.all()
        list_of_cities = []
        return_list_of_cities = []
        for key in obj:
            city_obj = key.replace('.', ' ')
            city_obj = shlex.split(city_obj)
            if city_obj[0] == 'City':
                list_of_cities.append(obj[key])
        for val in list_of_cities:
            if val.state_id == self.id:
                return_list_of_cities.append(val)
        return return_list_of_cities
