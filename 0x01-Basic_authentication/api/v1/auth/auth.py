#!/usr/bin/env python3
"""
This module contains authentication functions
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    This class contains authentication functions
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        This function checks if a path requires authentication
        """
        return False
    
    def authorization_header(self, request=None) -> str:
        """
        This function gets the authorization header from a request
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        This function gets the current user from a request
        """
        return None
