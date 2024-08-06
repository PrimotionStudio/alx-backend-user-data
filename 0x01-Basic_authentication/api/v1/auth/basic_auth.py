#!/usr/bin/env python3
"""
basic authentication
"""
import binascii
from base64 import b64decode
from .auth import Auth


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
