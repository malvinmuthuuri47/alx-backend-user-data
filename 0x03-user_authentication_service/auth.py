#!/usr/bin/env python3
"""This module performs password hashing"""

import bcrypt

def _hash_password(password: str) -> bytes:
    """This function handles the hashing part of the code by first
    converting the password to an array of bytes, then generating
    salt ant and hashing the bytes"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    return hash
