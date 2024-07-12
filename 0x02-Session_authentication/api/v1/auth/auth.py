#!/usr/bin/env python3
"""
This is authentication module longer long
"""


import os
#from flask import request
from typing import List, TypeVar


class Auth:
    """Authenticate me please
    how long do I  need"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """requires authenticatiion here, returns False """
        if excluded_paths is None:
            return True
        for pat in excluded_paths:
            if "*" in pat:
                patsplit = pat.split("*")
                if patsplit[0] in path:
                    return False
        if path in excluded_paths:
            return False
        if "/api/v1/status/" in excluded_paths and path == "/api/v1/status":
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """does nothing yet, returns none"""
        if request is None:
            return None
        authority = request.headers.get('Authorization')
        if authority is None:
            return None
        return authority

    def current_user(self, request=None) -> TypeVar('User'):
        """does nothing too, returns none"""
        return None

    def session_cookie(self, request=None):
        """returns cookie from a request"""
        if request is None:
            return None
        cookie = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie)
