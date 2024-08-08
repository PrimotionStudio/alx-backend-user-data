#!/usr/bin/env python3
"""
module for session auth
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


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
        self.user_id_by_session_id.update({session_id: user_id})
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns user_id based on session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> str:
        """
        returns a user obj based on cookie value"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        user = User.get(user_id)
        if user is None:
            return None
        return user

    def destroy_session(self, request=None):
        """
        destroys the session"""
        if request is None:
            return False
        cookie = self.session_cookie
        if cookie is None:
            return False
        if self.user_id_by_session_id.get(cookie) is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
