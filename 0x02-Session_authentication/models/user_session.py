#!/usr/bin/env python3
"""models/user_session.py"""
from .base import Base


class UserSession(Base):
    """models/user_session.py"""

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
