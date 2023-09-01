#!/usr/bin/env python3
"""Encrypting passwords"""

import bcrypt
from typing import ByteString


def hash_password(password: int) -> ByteString:
    """This function takes a password as an argument and performs
    a hashing on the function

    Returns:
            A byte string representing the hashed password"""
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    """This function checks if a password is equal to its equivalent
    byte string that has been passed through a hashing function

    Args:
        hashed_password: the hashed password
        password: The original password

    Returns:
        True if the hashed and original password match and False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
