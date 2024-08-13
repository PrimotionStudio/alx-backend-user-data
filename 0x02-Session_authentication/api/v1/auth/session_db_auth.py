#!/usr/bin/env python3
""".db_User.json"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """.db_User.json"""
    def create_session(self, user_id=None):
        """.db_User.json"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        UserSession.save_to_file()
        return session_id
