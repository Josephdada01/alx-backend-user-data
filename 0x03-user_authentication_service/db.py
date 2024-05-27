"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """
        method, which has two required string arguments:
        email and hashed_password, and returns a User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        # Add the user to the session
        self._session.add(new_user)
        # Commit the session to save changes
        self._session.commit()
        # Return the user instance
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        This method takes in arbitrary keyword arguments and returns the first
        row found in the users table as filtered by the method’s
        input arguments
        """
        try:
            # Query the User table with the provided keyword arguments
            user = self.__session.query(User).filter_by(**kwargs).one()
            # Raise NoResultFound if no result is found
        except NoResultFound:
            raise NoResultFound("Not found")
        # Raise InvalidRequestError for invalid query arguments
        except InvalidRequestError:
            raise InvalidRequestError("Invalid")
        # Return the found user
        return user

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
            # Find the user by user_id
            user = self.find_user_by(id=user_id)

            # Update the user's attributes
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")
            self._session.commit()
        except NoResultFound:
            raise NoResultFound("Not found")
        # Raise InvalidRequestError for invalid query arguments
        except InvalidRequestError:
            raise InvalidRequestError("Invalid")
