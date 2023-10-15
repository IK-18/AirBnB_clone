#!/usr/bin/python3
"""Defines the Place class"""
from models.base_model import BaseModel


class Place(BaseModel):
    """Initializes the Place class

    Attributes:
        city_id (str): city id
        user_id (str): user id
        name (str): place name
        description (str): place description
        number_rooms (int): number of rooms
        number_bathrooms (int): number of bathrooms
        max_guest (int): maximum number of guests
        price_by_night (int): price per night
        latitude (float): latitude position
        longitude (float): longitude position
        amenity_ids (list): list of amenity id
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
