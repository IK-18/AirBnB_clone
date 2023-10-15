#!/usr/bin/python3
"""Defines the FileStorage class"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Initializes the FileStorage class

    Attributes:
        __file_path (str): path to the JSON file
        __objects (dict): stores all objects by <class name>.id

    Methods:
        all(self): returns the dictionary objects
        new(self, obj): sets in __objects the obj with key <obj class name>.id
        save(self): serializes __objects to the JSON file
        reload(self): deserializes the JSON file to __objects
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects obj with key <obj_class_name>.id"""
        clname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(clname, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        objs = FileStorage.__objects
        obj_dict = {obj: objs[obj].to_dict() for obj in objs.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objs = json.loads(f.read())
                for obj in objs.values():
                    clname = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(clname)(**obj))
        except Exception:
            return
