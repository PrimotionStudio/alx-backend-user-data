#!/usr/bin/env python3
"""
This module contains authentication functions
"""
from flask import request
from typing import List, TypeVar
from markupsafe import escape


def slash_tolerant(path: str) -> str:
    """
    This function takes a path and returns a slash-tolerant version of it
    """
    if escape(path).endswith("/"):
        return escape(path)[:-1]
    if escape(path).endswith("*"):
        return escape(path)[:-1]
    return escape(path)


class Auth:
    """
    This class contains authentication functions
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        This function checks if a path requires authentication
        """
        path = slash_tolerant(path)
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        excluded_paths = [slash_tolerant(pth) for pth in excluded_paths]
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        This function gets the authorization header from a request
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This function gets the current user from a request
        """
        return None
