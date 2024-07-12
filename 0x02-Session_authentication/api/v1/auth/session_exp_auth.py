#!/usr/bin/env python3
"""
create expiry date for session.
"""

from os import getenv
from .session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """create an expiry session class"""

    def __init__(self) -> None:
        """overload parent class"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overload create session"""
        session = super().create_session(user_id)
        if session is None:
            return None
        sess_dict = {"user_id": user_id,
                     "created_at": datetime.now()
                     }
        self.user_id_by_session_id.update({session: sess_dict})
        return session

    def user_id_for_session_id(self, session_id=None):
        """overload method here"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            sess_dict = self.user_id_by_session_id.get(session_id)
            return sess_dict.get("user_id")
        created = self.user_id_by_session_id.get(session_id)
        created = created.get("created_at")
        if created is None:
            return None
        current = created + timedelta(seconds=self.session_duration)
        if datetime.now() > current:
            return None
        sess_dict = self.user_id_by_session_id.get(session_id)
        return sess_dict.get('user_id')
