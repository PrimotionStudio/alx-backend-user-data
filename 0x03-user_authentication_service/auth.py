#!/usr/bin/env python3
"""hashes a pasword with bcrypt"""
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
from uuid import uuid4


def _generate_uuid() -> str:
    """
    generates a random uuid
    """
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """
    function to hasha pwd"""
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            if not isinstance(password, bytes):
                password = _hash_password(password)
            return self._db.add_user(email, password)

    def valid_login(self, email: str, password: str) -> bool:
        """validate if input creedentials is correct"""
        try:
            user = self._db.find_user_by(email=email)
            if not checkpw(password.encode("utf-8"), user.hashed_password):
                return False
        except NoResultFound:
            return False
        return True

    def create_session(self, email: str) -> str:
        """
        creates a session for the user
        """
        user = self._db.find_user_by(email=email)
        user_id = user.id
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
