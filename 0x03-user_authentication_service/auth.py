#!/usr/bin/env python3
"""hashes a pasword with bcrypt"""
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


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

    def valid_login(self, email, password):
        """validate if input creedentials is correct"""
        try:
            user = self._db.find_user_by(email=email)
            if not checkpw(password.encode("utf-8"), user.hashed_password):
                return False
        except NoResultFound:
            return False
        return True
