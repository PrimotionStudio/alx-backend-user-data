#!/usr/bin/env python3
"""
basic authentication
"""
import binascii
from base64 import b64decode
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Basic Auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header):
        """
        Extracts the base64 encoded part of the Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header):
        """
        Decodes the base64 encoded Authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            result = b64decode(base64_authorization_header,
                               validate=False)
            return result.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header):
        """
        Extracts the user credentials from
        the decoded Authorization header
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        auth_obj = decoded_base64_authorization_header.split(":")
        return auth_obj[0], auth_obj[1]

    def user_object_from_credentials(self, user_email, user_pwd):
        """
        Creates a user object from the user credentials
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if len(users) <= 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None
