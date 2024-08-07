#!/usr/bin/env python3
""" authorization class """

from flask import request
from typing import List, TypeVar


class Auth:
    """ template for all authentication system"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ first stage"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        new_path = ''
        if path[-1] != '/':
            new_path = path + '/'
        if path in excluded_paths or new_path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header"""
        if request is None:
            return None
        header = request.header.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        return None
