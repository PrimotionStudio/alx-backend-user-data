#!/usr/bin/env python3
"""hashes a pasword with bcrypt"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    function to hasha pwd"""
    return hashpw(password.encode('utf-8'), gensalt())
