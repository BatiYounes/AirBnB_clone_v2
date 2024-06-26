#!/usr/bin/python3
"""place class definition"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id number.
        user_id: user id number.
        name: city name.
        description: city description.
        number_rooms: number of room availlable.
        number_bathrooms: number of bathrooms availlable.
        max_guest: maximum guest number.
        price_by_night:: pice for one night.
        latitude: latitude in float.
        longitude: longitude in float.
        amenity_ids: list of Amenity_ids
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="place")

        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """returns list of reviews.id"""
            review_obj = models.storage.all()
            list_review = []
            return_list = []
            for key in review_obj:
                _review = key.replace('.', ' ')
                _review = shlex.split(_review)
                if _review[0] == 'Review':
                    list_review.append(review_obj[key])
            for val in list_review:
                if (val.place_id == self.id):
                    return_list.append(val)
            return return_list

        @property
        def amenities(self):
            """returns list of amenity_ids"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """appends amenity_ids to the attribute """
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
