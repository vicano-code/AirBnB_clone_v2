#!/usr/bin/python3

"""
database storage engine
"""
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.state import State
from models.city import City
from models.base_model import Base


class DBStorage:
    """database storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """initialise storage attributes"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env_ = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if env_ == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query current database session"""
        db_dict = {}

        if cls != "":
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
            return db_dict
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(v).all()
                    if len(objs) > 0:
                        for obj in objs:
                            key = "{}.{}".format(obj.__class__.__name__,
                                                 obj.id)
                            db_dict[key] = obj
            return db_dict

    def new(self, obj):
        """Adds new object to current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of current database session"""
        self.__session.commit()

    def reload(self):
        """create session & load table from database"""
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def delete(self, obj=None):
        """Delete from current database session"""
        if obj is not None:
            self.__session.delete(obj)
