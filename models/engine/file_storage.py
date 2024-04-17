#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    class_dic = {"BaseModel": BaseModel,
                 "User": User,
                 "State": State,
                 "City": City,
                 "Amenity": Amenity,
                 "Place": Place,
                 "Review": Review}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects

        filtered_obj = {}
        for key, val in self.__objects.items():
            if cls.__name__ in key:
                filtered_obj[key] = val
        return filtered_obj

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        obj_dict = {}
        for key, obj in self.__objects.items():
            if type(obj) is dict:
                obj_dict[key] = obj
            else:
                obj_dict[key] = obj.to_dict()
        with open(self.__file_path, mode="w", encoding="utf-8") as json_file:
            json.dump(obj_dict, json_file)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, "r") as json_file:
                json_obj = json.load(json_file)
            for key, obj in json_obj.items():
                obj = self.class_dic[obj['__class__']](**obj)
                self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
        Delete an object
        '''
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            self.__objects.pop(key, None)
            self.save()

    @property
    def cities(self):
        """returns the list of City instances"""

