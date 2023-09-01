#!/usr/bin/env python3
"""Encrypting passwords"""

import bcrypt
from typing import ByteString


def hash_password(password) -> ByteString:
    """This function takes a password as an argument and performs
    a hashing on the function

    Returns:
            A byte string representing the hashed password"""
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pass
