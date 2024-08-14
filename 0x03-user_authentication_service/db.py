#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
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
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ returns a User object """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except Exception as e:
            self._session.rollback()
            raise e

    def find_user_by(self, **kwargs) -> User:
        """ takes in arbitrary keyword arguments
        returns the first row found in the users"""
        all_users = self._session.query(User)
        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise InvalidRequestError
            for user in all_users:
                if getattr(user, k) == v:
                    return user
        raise NoResultFound

    def update_user(self, id: int, **kwargs) -> None:
        """ finds and updates a user"""
        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise ValueError
            try:
                user = self.find_user_by(id=id)
                setattr(user, k, v)
                return None
            except InvalidRequestError or NoResultFound:
                raise ValueError
