#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoize the session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds and return user to and from database"""
        new = User()
        new.email = email
        new.hashed_password = hashed_password
        Session = self._session
        Session.add(new)
        Session.commit()
        return new

    def find_user_by(self, **kwargs) -> User:
        """find user and return"""
        Session = self._session
        Query = Session.query(User).filter_by(**kwargs)
        if Query.first() is None:
            raise NoResultFound
        return Query.first()

    def update_user(self, user_id: int, **kwargs) -> None:
        """update the user’s attributes as passed in the method’s arguments"""
        Session = self._session
        update_me = self.find_user_by(id=user_id)
        update_dict = update_me.__dict__
        for attr in kwargs:
            if attr not in update_dict:
                raise ValueError
            setattr(update_me, attr, kwargs[attr])
            Session.flush()
        Session.commit()
