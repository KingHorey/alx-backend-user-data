#!/usr/bin/env python3
"""
Hashes a password
"""


from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """You alakobian. I will commemt"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user to database"""
        db = self._db
        try:
            check = db.find_user_by(email=email)
            raise ValueError("User <user's email> already exists")
        except NoResultFound:
            password = _hash_password(password)
            return db.add_user(email, password)

    def valid_login(self, email: str, password: str) -> bool:
        """checks if passwodd is falid"""
        import bcrypt
        db = self._db
        try:
            user = db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """creates session id for email"""
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except Exception:
            return None
        uid = _generate_uuid()
        db.update_user(user.id, session_id=uid)
        return uid

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        If the session ID is None or no user is found, return None.
        Otherwise return the corresponding user.
        """
        db = self._db
        if session_id is not None:
            try:
                user = db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                pass
        return None

    def destroy_session(self, user_id: int) -> None:
        """ updates the corresponding user’s session ID to None"""
        db = self._db
        db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """resets the password"""
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """reset password from token"""
        db = self._db
        try:
            user = db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        password = _hash_password(password)
        db.update_user(user.id, hashed_password=password, reset_token=None)


def _hash_password(password: str) -> bytes:
    """returns a byted hashed password"""
    import bcrypt

    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """generate uuid in string"""
    import uuid
    return str(uuid.uuid4())
