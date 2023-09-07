#!/usr/bin/env python3
"""Empty session"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """This function creates a Session id for a user_id

        Args:
            user_id : The user_id to create a Session id for

        Returns:
            The session id for the user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        else:
            id = str(uuid.uuid4())
            SessionAuth.user_id_by_session_id[id] = user_id
            return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """This method returns a user ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        else:
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """This function returns a User instance based on a cookie value
        Methodology:
            1. Obtain the cookie value from the request
            2. Use the cookie value to obtain the session ID
            3. Use the session ID to obtain the associated User ID
            4. Use the user ID to fetch the User instance
        """
        cookie_val = self.session_cookie(request)
        if cookie_val is None:
            return None
        session_id = cookie_val
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user = User.get(user_id)
        return user
