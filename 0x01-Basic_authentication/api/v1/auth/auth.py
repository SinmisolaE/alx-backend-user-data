#!/usr/bin/env python3
""" authorization class """

from flask import request
from typing import List, TypeVar


class Auth:
    """ template for all authentication system"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ first stage"""
        return False

    def authorization_header(self, request=None) -> str:
        """ aithorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        return None
