#!/usr/bin/env python3
"""Basic auth module"""

from api.v1.auth.auth import Auth


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
