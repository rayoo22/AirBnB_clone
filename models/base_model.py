#!/usr/bin/python3
"""Module BaseModel"""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """contents of the BaseModel class"""
    def __init__(self, *args, **kwargs):
        """
        Args:
            id: id for every base_model instance createad
            created_at: attribute for datetime an instance was created
            updated_at: "" for datetime an instance was created and updated
        """
        if kwargs:
            """if kwargs is not empty"""
            for key, val in kwargs.items():
                if 'created_at' ==  key:
                    self.created_at = datetime.strptime(kwargs['created_at'], "%Y-%m-%dT%H:%M:%S.%f")
                elif 'updated_at' == key:
                    self.updated_at = datetime.strptime(kwargs['updated_at'], "%Y-%m-%dT%H:%M:%S.%f")
                elif '__class__' == key:
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """string representation of basemodel object"""
        return f'[{self.__class__.__name__}] {(self.id)} {self.__dict__}'

    def save(self):
        """updates updated_at attr with current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """dictionary representation with key/value of BaseModel instance"""
        dict = {}
        dict["__class__"] = self.__class__.__name__
        for k, v in self.__dict__.items():
            if isinstance(v, (datetime, )):
                dict[k] = v.isoformat()
            else:
                dict[k] = v
        return dict
