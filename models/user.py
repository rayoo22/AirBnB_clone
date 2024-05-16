#!/usr/bin/python3
"""user module"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    user class inheriting from BaseModel
    public class attributes for the User class
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
