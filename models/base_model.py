#!/usr/bin/python3
"""Defines all common attributes/methods for other classes"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Instantiates the basemodel for all other classes.

    Attributes:
        id (string): unique uuid identifier
        created_at (datetime): current datetime when an instance is created
        updated_at (datetime): current datetome when an instance is updated
    """

    def __init__(self, *args, **kwargs):
        """Initializes an instance of BaseModel

        Args:
            args (any): Unused
            kwargs (dict): Key/Value pairs of attributes

        Methods:
            save(self): updates updated_at withe the current datetime
            to_dict(self): returns an updated dict version of the instance
        """
        dateform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if (len(kwargs) != 0):
            for k, v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    self.__dict__[k] = datetime.strptime(v, dateform)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """Updates updated_at with the current datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return an updated dict version of the instance"""
        new_dict = self.__dict__.copy()
        new_dict.update({"__class__": self.__class__.__name__})
        new_dict.update({"created_at": self.created_at.isoformat()})
        new_dict.update({"updated_at": self.updated_at.isoformat()})
        return new_dict

    def __str__(self):
        """Returns string representaion of instance"""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
