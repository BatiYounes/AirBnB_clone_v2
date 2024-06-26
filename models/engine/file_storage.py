#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format
    Attributes:
        __file_path: JSON file path
        __objects: objects dictionary
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        _dict = {}
        if cls:
            _dict_ = self.__objects
            for key in _dict_:
                _dict_partition = key.replace('.', ' ')
                _dict_partition = shlex.split(_dict_partition)
                if (_dict_partition[0] == cls.__name__):
                    _dict[key] = self.__objects[key]
            return _dict
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary
        Args:
            obj: given object
        """
        if obj:
            key = f'{type(obj).__name__}.{obj.id}'
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        _dict = {}
        for key, value in self.__objects.items():
            _dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(_dict, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete object from a list of objects."""
        if obj:
            obj_to_delete = f'{type(obj).__name__}.{obj.id}'
            del self.__objects[obj_to_delete]

    def close(self):
        """calls reload method for deserializing the JSON file
        to objects"""
        self.reload()
