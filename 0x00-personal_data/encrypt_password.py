#!/usr/bin/env python3
"""
This module contains the function to hash passwords.
"""
import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hash a password with a random salt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
