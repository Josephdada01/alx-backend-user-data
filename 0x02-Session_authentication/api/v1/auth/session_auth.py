#!/usr/bin/env python3
"""Modules of class SessionAuth that inherits from Auth."""
import uuid
from api.v1.auth.auth import Auth


"""the first 2 methods (create_session and user_id_for_session_id)
for storing and retrieving a link between a User ID and a Session ID.
"""


class SessionAuth(Auth):
    """a session class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """an instance method that creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """method that returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
