#!/usr/bin/python3
"""Module BaseModel"""
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """contents of the BaseModel class"""
    def __init__(self, **kwargs):
        """
        Args:
            id: id for every base_model instance createad
            created_at: attribute for datetime an instance was created
            updated_at: "" for datetime an instance was created and updated
        """
        if kwargs:
            """if kwargs is not empty"""
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
            if 'created_at' in kwargs:
                self.created_at = datetime.strptime(kwargs['created_at'], "%Y-%m-%dT%H:%M:%S.%f")
            if 'updated_at' in kwargs:
                self.updated_at = datetime.strptime(kwargs['updated_at'], "%Y-%m-%dT%H:%M:%S.%f")
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        """string representation of basemodel object"""
        return f'[{self.__class__.__name__}] {(self.id)} {self.__dict__}'

    def save(self):
        """updates updated_at attr with current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """dictionary representation with key/value of BaseModel instance"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
