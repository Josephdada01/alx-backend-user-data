#!/usr/bin/env python3
"""Implementing a custom authentication"""
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """class to manage basic api"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """a public methods"""
        if path is None:
            return True
        if not excluded_paths:
            return True
        # Normalize path by ensuring it ends with a slash
        normal_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            n_excluded_path = (excluded_path if excluded_path.endswith('/')
                               else excluded_path + '/')
            if normal_path == n_excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """a public methods"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ a public method"""
        return None
