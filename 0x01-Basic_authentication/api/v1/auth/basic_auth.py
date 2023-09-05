#!/usr/bin/env python3
"""Basic auth module"""

from api.v1.auth.auth import Auth
import binascii
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Class Basic Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """This function returns the Base64 part of the authorization header
        for a basiic authentication provided that the authorization header
        passes the criteria

        Requirements:
            - authorization_header should not be None
            - authorization_header should be an instance of str
            - authorization header should start with Basic and have
              a space between Basic and the next word

        Returns:
            - The Base64 part of the authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.startswith("Basic"):
            words = authorization_header.split()

            if len(words) >= 2:
                return words[1]
            return
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """This function decodes bytes into utf-8 encoded strings provided:

        Arguments:
            base64_authorization_header: bytes str

        Requirements:
            - Return None if base64_authorization_header is None
            - Return None if base64_authorization_header is not an
              instance of str
            - Try to decode base64_authorization_header from a Base64str to
              a UTF8 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(
                    base64_authorization_header.encode('utf-8')
                    )
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except (binascii.Error, UnicodeDecodeError, TypeError):
            return None
        return

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """This function returns a tuple with either the values present in the
        decoded string or None if the values in the decoded string don't pass
        the criteria

        Requirements:
            - If decoded string is None, return None
            - If decoded string is not an instance of a string, return None
            - If : is present in the decoded string, split the string using
              the colon as the delimiter and return the split string in a
              tuple otherwise if the : isn't present, return a tuple whose
              values are None
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' in decoded_base64_authorization_header:
            parts = decoded_base64_authorization_header.split(':', 1)

            part1 = parts[0]
            part2 = parts[1]

            return (part1, part2)
        else:
            return (None, None)
        return

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """This function searches the database file for instances that
        contain the email and password provided.

        Requirements:
            - If user_email is None or not a string, return None
            - If user_pwd is None or not a string, return None
            - Search for instances of the User class and if none are
              found, return None.
            - Return None if the password is not valid for the User
              instance found
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
