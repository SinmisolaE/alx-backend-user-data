#!/usr/bin/env python3
"""
  method that takes in a password string arguments and returns bytes
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ eturned bytes is a salted hash of the input password
      hashed with bcrypt.hashpw
    """
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


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
