#!/usr/bin/env python3
"""A module that contains a class that manages the API authentication"""

from flask import request
from typing import List, TypeVar


class Auth:
    """This class contains all the functions that manage the API
    authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth function checks which routes don't need
        authentication
        """
        if path is None:
            return True
        if excluded_paths is None or []:
            return True
        if path in excluded_paths:
            return False
        if not path.endswith('/'):
            path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """authorization_header function"""
        if request is None:
            return None
        else:
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                return None
            else:
                return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user function"""
        return None

    def session_cookie(self, request=None):
        """This function returns a cookie value from a request"""
        if request is None:
            return None
        else:
            return request.cookies.get('_my_session_id')
