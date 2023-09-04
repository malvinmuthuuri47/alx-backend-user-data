#!/usr/bin/env python3
"""A module that contains a class that manages the API authentication"""

from flask import request
from typing import List, TypeVar


class Auth:
    """This class contains all the functions that manage the API
    authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth function"""
        return False

    def authorization_header(self, request=None) -> str:
        """authorization_header function"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user function"""
        return None
