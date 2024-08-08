#!/usr/bin/env python3
"""
module for session auth
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    class for session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create a session id for user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = uuid4()
        SessionAuth.user_id_by_session_id.update({session_id: user_id})
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns user_id based on session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)
