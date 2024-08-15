#!/usr/bin/env python3
"""
  method that takes in a password string arguments and returns bytes
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """ eturned bytes is a salted hash of the input password
      hashed with bcrypt.hashpw
    """
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """ return a string representation of a new UUID. """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
          return a User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hash_password = _hash_password(password)
            user = self._db.add_user(email, hash_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate password of a user"""
        try:
            user = self._db.find_user_by(email=email)
            user_pass = user.hashed_password
            hash_pass = password.encode('utf-8')
            return bcrypt.checkpw(hash_pass, user_pass)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ takes an email string argument
          returns the session ID as a string
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """ takes a single session_id string argument
        returns the corresponding User or None."""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return User

    def destroy_session(user_id: int) -> None:
        """ updates the corresponding user’s session ID to None"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

