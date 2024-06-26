#!/usr/bin/python3
"""DBStorage module."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """DBStorage class to store and retrieve data from database."""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, db),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """this method must return a dictionary: (like FileStorage)"""
        obj_dictionary = {}
        if cls is None:
            class_list = [User, State, City, Amenity, Place, Review]
            for clss in class_list:
                query = self.__session.query(clss)
                for obj in query:
                    key = f'{type(obj).__name__}.{obj.id}'
                    obj_dictionary[key] = obj
        else:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = f'{type(obj).__name__}.{obj.id}'
                obj_dictionary[key] = obj
        return obj_dictionary

    def new(self, obj):
        """this method add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """this method commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """this method delete from the current database session obj"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """this method create or reload the current database session"""
        Base.metadata.create_all(self.__engine)
        curr_sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(curr_sess)
        self.__session = Session()

    def close(self):
        """calls remove method on the private session to close it."""
        self.__session.close()
