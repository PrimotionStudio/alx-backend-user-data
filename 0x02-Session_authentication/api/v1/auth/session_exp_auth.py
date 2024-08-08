#!/usr/bin/env python3
"""
session expiry
"""
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    session expiry auth"""
    def __init__(self):
        """
        inistialize"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create an expiry session"""
        session_id = super().create_session(user_id)
        if not isinstance(session_id, str):
            return None
        self.user_id_by_session_id.update({session_id: {
                                                        "user_id": user_id,
                                                        "created_at": datetime.now()
                                                       }})
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ get user_id from session_id"""
        if session_id is None:
            return None
        if session_id not in user_id_by_session_id.keys():
            return None
        session = user_id_by_session_id[session_id]
        if "created_at" not in session.keys():
            return None
        cur_time = datetime.now()
        duration = timedelta(seconds=self.session_duration)
        exp_time = int(session["created_at"]) + duration
        if exp_time < cur_time:
            return None

        if self.session_duration <= 0:
            return session.get(user_id)
