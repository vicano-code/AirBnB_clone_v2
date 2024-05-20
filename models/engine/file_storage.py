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

    class_dic = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects

        if cls != "":
            filtered_obj = {}
            for key, val in self.__objects.items():
                if cls == key.split(".")[0]:
                    filtered_obj[key] = val
            return filtered_obj
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        obj_dict = {}
        for key, obj in FileStorage.__objects.items():
                obj_dict[key] = obj.to_dict()
        with open(FileStorage.__file_path, mode="w",
                  encoding="utf-8") as json_file:
            json.dump(obj_dict, json_file)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, "r") as json_file:
                self.__objects = json.load(json_file)
            for key, obj in self.__objects.items():
                obj = self.class_dic[obj['__class__']](**obj)
                self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete an object"""
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            self.__objects.pop(key, None)
            self.save()

    def close(self):
        """deserializing the JSON file to objects"""
        self.reload()
