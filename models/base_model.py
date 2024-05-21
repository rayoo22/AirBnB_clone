#!/usr/bin/python3
"""Module BaseModel"""

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """
    BaseModel is a base class that defines
        -common attributes/methods for other classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the instance.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key,
                            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                elif key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the instance
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        Updates the updated_at attribute with the current datetime
            saves the instance to models.storage.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the instance.
        """
        dict = self.__dict__.copy()
        dict['__class__'] = self.__class__.__name__
        dict['created_at'] = self.created_at.isoformat()
        dict['updated_at'] = self.updated_at.isoformat()
        return dict

    @classmethod
    def all(cls):
        """
        Class method that returns a list of all instances
            of the class from models.storage.
        """
        return [instance for instance in models.storage.all().values()
                if isinstance(instance, cls)]
