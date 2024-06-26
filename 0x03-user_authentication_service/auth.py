#!/usr/bin/env python3
"""Hash password module"""
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    method that takes in a password string arguments
    and returns bytes.
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw.
    """
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    """private function that return a string
    representation of a new UUID"""
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """This method register a user and if the user exist
        If a user already exist with the passed email, raise a ValueError.
        if email in self._db:
            raise ValueError(f"User {email} already exist")
        if no user using the email, hash the pass word and save it
        hash_password = self._hash_password(password)
        new_user = User(email, hash_password)
        self._db[email] = new_user
        return new_user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError(f"User {email} already exist")

    def valid_login(self, email: str, password: str) -> bool:
        """mplement the Auth.valid_login method. It should expect email and
        password required arguments and return a boolean.
        Try locating the user by email.
        If it exists, check the password with bcrypt.checkpw.
        If it matches return True.
        In any other case, return False."""
        try:
            # find the user in our database
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode('utf-8'),
                                       user.hashed_password):
                return True
            else:
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """This method creates a session ID for the
        user identified by the email."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
            else:
                return None
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Auth.get_user_from_session_id method. It takes a single session_id
        string argument and returns the corresponding User or None.
        If the session ID is None or no user is found, return None.
        Otherwise return the corresponding user.
        Remember to only use public methods of self._db."""
        try:
            if session_id is None:
                return None
            else:
                user = self._db.find_user_by(session_id=session_id)
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """The method updates the corresponding user’s session ID to None."""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None

    def get_reset_password_token(self, email: str) -> str:
        """function Generate reset password token
        It take an email string argument and returns a string.
        Find the user corresponding to the email. If the user does not
        exist, raise a ValueError exception. If it exists, generate a UUID
        and update the user’s reset_token database field. Return the token."""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password using the reset_token.

        :param reset_token: The reset token provided to the user.
        :param password: The new password to set for the user.
        :raises ValueError: If no user is found with the given reset_token.
        """
        try:
            # Find the user by the reset token
            user = self._db.find_user_by(reset_token=reset_token)
            # Hash the new password
            hashed_password = _hash_password(password)
            # Update the user's password and reset the reset_token to None
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            # Raise a ValueError if no user is found with the provided
            # reset_token
            raise ValueError
