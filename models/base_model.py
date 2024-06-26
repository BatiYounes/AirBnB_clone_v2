#!/usr/bin/python3
"""BaseModel class definition."""
from sqlalchemy.ext.declarative import declarative_base
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class BaseModel:
    """BaseModel class def."""
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """Instantiation of base model class
        Args:
            args: it won't be used
            kwargs: pointer to the list of args.
        Attributes:
            id: unique id.
            created_at: created datetime.
            updated_at: updated datetime.
        """
        if kwargs:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    val = datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, val)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """returns a string of class name, id, and dictionary."""
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        """return a string representaion."""
        return self.__str__()

    def save(self):
        """updates the public instance attribute updated_at to
        current datetime and save it in the storage.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """creates dictionary of the class and returns
        dictionary of all the key values in __dict__
        """
        _dict = dict(self.__dict__)
        _dict["__class__"] = str(type(self).__name__)
        _dict["created_at"] = self.created_at.isoformat()
        _dict["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in _dict.keys():
            del _dict['_sa_instance_state']
        return _dict

    def delete(self):
        """ delete object from storage."""
        models.storage.delete(self)
