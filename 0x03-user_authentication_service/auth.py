#!/usr/bin/env python3
"""This module performs password hashing"""

import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {email} already exists.")
        except NoResultFound:
            passwd = _hash_password(password)
            user = self._db.add_user(email, passwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """This function searches for a user by email and if the user
        exists, it checks the password hash. If if matches, it returns
        true and false otherwise."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                # print(user.hashed_password)
                passwd_bytes = password.encode('utf-8')
                hashed_passwd = user.hashed_password
                if bcrypt.checkpw(passwd_bytes, hashed_passwd):
                    return True
                return False
        except Exception:
            return False


def _hash_password(password: str) -> bytes:
    """This function handles the hashing part of the code by first
    converting the password to an array of bytes, then generating
    salt ant and hashing the bytes"""
    bytes_passwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(bytes_passwd, salt)

    return hashed_passwd
