#!/usr/bin/python3
"""FileStorage module"""
import json
import os.path as path
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    A class FileStorage that serializes instances to a JSON file
    and deserializes JSON file to instances.

    Attributes:
        __file_path (str): The file path to the JSON file.
        __objects (dict): The dictionary of objects.
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects.

        Returns:
            dict: The dictionary of objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.

        Args:
            obj (BaseModel): The object to add to __objects.
        """
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        my_dict = {}

        with open(self.__file_path, mode='w', encoding='UTF-8') as f:
            for key, obj in self.__objects.items():
                my_dict[key] = obj.to_dict()
            json.dump(my_dict, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists ; otherwise, do nothing).
        """
        try:
            if path.isfile(self.__file_path):
                with open(self.__file_path, mode='r', encoding='UTF-8') as f:
                    for key, value in json.load(f).items():
                        value = eval(value['__class__'])(**value)
                        self.__objects[key] = value
        except FileNotFoundError:
            pass
