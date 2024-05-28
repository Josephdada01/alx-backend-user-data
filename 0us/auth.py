#!/usr/bin/env python3
"""Hash password module"""
import bcrypt


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

def find_user_by(self, **kwargs) -> User:
        """
        This method takes in arbitrary keyword arguments and returns the first
        row found in the users table as filtered by the method’s
        input arguments
        """
        # Query the User table with the provided keyword arguments
        all_users = self.__session.query(User)
        for key, val in kwargs.items():
            if key not in User.__dict__:
                # if the query is bad raise Invlid request
                raise InvalidRequestError
            for user in all_users:
                if getattr(user, key) == val:
                    return user
        # raise no result if no result is found
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs):
        """
        method that takes as argument a required user_id integer and
        arbitrary keyword arguments, and returns None.
        The method will use find_user_by to locate the user to update,
        then will update the user’s attributes as passed in the method’s
        arguments then commit changes to the database.
        If an argument that does not correspond to a user attribute is passed,
        raise a ValueError
        """
        try:
            usr = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for k, v in kwargs.items():
            if hasattr(usr, k):
                setattr(usr, k, v)
            else:
                raise ValueError
        self._session.commit()
