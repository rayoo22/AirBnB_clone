#!/usr/bin/python3
"""FileStorage module"""
import json
import os.path as path
from models.base_model import BaseModel


class FileStorage:
    """serializes instances to a JSON file
        and deserializes JSON file to instances
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """ returns the dictionary __objects """
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        my_dict = {}

        with open(self.__file_path, mode='w', encoding='UTF-8') as f:
            for key, obj in self.__objects.items():
                """
                if type(obj) is a dictionary:
                    my_dict[key] = obj
                else:
                """
                my_dict[key] = obj.to_dict()
            json.dump(my_dict, f)

    def reload(self):
        """ deserializes the JSON file to __objects"""
        try:
            if path.isfile(self.__file_path):
                with open(self.__file_path, mode='r', encoding='UTF-8') as f:
                    for key, value in json.load(f).items():
                        value = eval(value['__class__'])(**value)
                        self.__objects[key] = value
        except FileNotFoundError:
            pass
