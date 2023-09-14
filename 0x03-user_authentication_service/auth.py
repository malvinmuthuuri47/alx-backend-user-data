#!/usr/bin/env python3
"""This module performs password hashing"""

import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


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

    def create_session(self, email: str) -> str:
        """This function takes email as an argument and finds the user
        corresponding to the email, generates a new UUID and stores it
        in the database as the user's session_id.

        Returns:
            - The Session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id_str = str(uuid.uuid4())
                self._db.update_user(user_id=user.id,
                                     session_id=session_id_str)
                return session_id_str
        except Exception as e:
            return

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """This function finds a user by session ID and either returns a user
        or returns None"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            if not session_id or not user:
                return None
            else:
                return user
        except Exception:
            return

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                user.session_id = self._db.update_user(user_id=user.id,
                                                       session_id=None)
            return None
        except Exception as e:
            print(e)

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            user_uuid = _generate_uuid()
            self._db.update_user(user.id, reset_token=user_uuid)
            return user_uuid
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """This function handles the hashing part of the code by first
    converting the password to an array of bytes, then generating
    salt ant and hashing the bytes"""
    bytes_passwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(bytes_passwd, salt)

    return hashed_passwd


def _generate_uuid() -> str:
    """This function generates UUIDs and returns that string"""
    uuid_str = str(uuid.uuid4())
    return uuid_str
