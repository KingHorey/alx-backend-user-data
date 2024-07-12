#!/usr/bin/env python3
"""authentication for session"""


from .auth import Auth
import uuid


import sys
import os
parent_dir = os.path.abspath(os.path.join('models'))
sys.path.insert(0, parent_dir)


class SessionAuth(Auth):
    """
    validate if everything inherits correctly without any overloading
    validate the “switch” by using environment variables
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """that creates a Session ID for a user_id"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        uid = str(uuid.uuid4())
        self.user_id_by_session_id.update({uid: user_id})
        return uid

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> int:
        """returns user based on cookies"""
        from models.user import User
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """destroys session and returns a boolean value"""
        if request is None:
            return False
        if not self.session_cookie(request):
            return False
        if not self.user_id_for_session_id(self.session_cookie(request)):
            return False
        key = self.user_id_for_session_id(self.session_cookie(request))
        sessions = self.user_id_by_session_id.copy()
        for uid in sessions:
            if sessions.get(uid) == key:
                self.user_id_by_session_id.pop(uid)
        return True
