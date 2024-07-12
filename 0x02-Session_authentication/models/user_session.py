#!/usr/bin/env python3
"""stores session in database"""


from .base import Base
import uuid


class UserSession(Base):
    """usersession class for db"""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """initializes the class"""
        super().__init__(*args, **kwargs)
        try:
            self.user_id: str = kwargs["user_id"]
        except KeyError:
            pass
        if "session_id" not in kwargs:
            self.session_id = str(uuid.uuid4())
        else:
            self.session_id = kwargs['session_id']
