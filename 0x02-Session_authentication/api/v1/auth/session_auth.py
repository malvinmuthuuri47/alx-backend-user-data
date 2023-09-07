#!/usr/bin/env python3
"""Empty session"""
from api.v1.auth.auth import Auth
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
