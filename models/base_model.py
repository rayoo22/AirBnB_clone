#!/usr/bin/python3
"""Module BaseModel"""

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """
    BaseModel is a base class that defines
        -common attributes/methods for other classes.

    Attributes:
        id (str): Unique identifier for each instance
                    assigned with a UUID when an instance is created.
        created_at (datetime): The date and time when an instance is created
                                assigned with the current datetime.
        updated_at (datetime): The date and time when an instance is updated
                                assigned with the current datetime.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the instance.
        If kwargs are provided
            it sets the attributes according to the key-value pairs in kwargs.
        If kwargs is not provided
            it generates a unique id using uuid4()
                sets created_at and updated_at to the current datetime.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if kwargs:
            for key, value in kwargs.items():
                if 'created_at' == key:
                    self.created_at = datetime.strptime
                    (kwargs['created_at'], "%Y-%m-%dT%H:%M:%S.%f")
                elif 'updated_at' == key:
                    self.updated_at = datetime.strptime
                    (kwargs['updated_at'], "%Y-%m-%dT%H:%M:%S.%f")
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
        """
        Returns a string representation of the instance
            including the class name, id, and dictionary of the instance.

        Returns:
            str: A string representation of the instance.
        """
        return f'[{self.__class__.__name__}] {(self.id)} {self.__dict__}'

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
        It adds the class name under the key __class__,
        and converts datetime objects to ISO format strings.

        Returns:
            dict: A dictionary representation of the instance.
        """
        dict = {}
        dict["__class__"] = self.__class__.__name__
        for k, v in self.__dict__.items():
            if isinstance(v, (datetime, )):
                dict[k] = v.isoformat()
            else:
                dict[k] = v
        return dict

    @classmethod
    def all(cls):
        """
        Class method that returns a list of all instances
            of the class from models.storage.

        Returns:
            list: A list of all instances of the class.
        """
        from models import storage
        instances = storage.all().values()
        return [instance for instance in instances
                if isinstance(instance, cls)]
