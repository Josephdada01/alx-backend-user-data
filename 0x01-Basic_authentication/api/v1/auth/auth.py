#!/usr/bin/env python3
"""Implementing a custom authentication"""
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """class to manage basic api"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """a public method"""
        return False

    def authorization_header(self, request=None) -> str:
        """a public methods"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ a public method"""
        return None
