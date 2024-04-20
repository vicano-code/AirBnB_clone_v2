#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

    @property
    def cities(self):
        """
        Return list of city instances if City.state_id==current
        State.id
        FileStorage relationship between State and City
        """
        list_cities = []
        for city in models.storage.all("City").values():
            if city.state_id == self.id:
                list_cities.append(city)
        return list_cities
