#!/usr/bin/env python3
"""
Basic Authentication, child of Auth
"""
from .auth import Auth
from typing import TypeVar
import os
import sys


parent_dir = os.path.abspath(os.path.join('models'))
sys.path.insert(0, parent_dir)


class BasicAuth(Auth):
    """A basic authentity class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 authorizzation header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if "Basic " not in authorization_header:
            return None
        else:
            return authorization_header.replace("Basic ", "")

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """decode base 64"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        import base64
        try:
            return base64.b64decode(
                    base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """returns tuple of username and email"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        split = decoded_base64_authorization_header.split(":", 1)
        return (split[0], split[1])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns users based on email"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        from models.user import User
        from models.base import DATA
        User.load_from_file()
        for uses in DATA['User']:
            if DATA['User'][uses].email == user_email:
                if DATA['User'][uses].is_valid_password(user_pwd):
                    return DATA['User'][uses]
                return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a user after validation"""
        authority64 = self.authorization_header(request)
        user64 = self.extract_base64_authorization_header(authority64)
        user = self.decode_base64_authorization_header(user64)
        user = self.extract_user_credentials(user)
        user = self.user_object_from_credentials(user[0], user[1])
        return user
