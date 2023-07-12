#!/usr/bin/python3
"""DB storage engine"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = (City, Place, State, User, Review)


class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """initialize a DBStorage instance"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        conn_str = 'mysql+mysqldb://{}:{}@{}/{}'.format(
                user, passwd, host, database)
        self.__engine = create_engine(conn_str, pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all models currently in storage
        if cls is given, return only objects from with class cls"""
        dct = {}
        if cls:
            query = self.__session.query(cls)
            for obj in query.all():
                key = "{}.{}".format(cls.__name__, obj.id)
                dct[key] = obj
        else:
            for x in classes:
                query = self.__session.query(x)
                for obj in query.all():
                    key = "{}.{}".format(x.__name__, obj.id)
                    dct[key] = obj
        return dct

    def new(self, obj):
        """Add obj to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if obj is not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload the database session:
        - create all tables in the database
        - create the current database session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
