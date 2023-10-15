#!/usr/bin/python3
"""Defines the Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Initializes the Review class

    Attributes:
        place_id (str): place id
        user_id (str): user id
        text (str): review text
    """

    place_id = ""
    user_id = ""
    text = ""
