#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

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
        """This method saves a new user to the database

        Returns:
            - A User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """This method return the first row found in the users table as
        filtered by the method's input arguments
        """
        if not kwargs:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).one()

        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """This function updates the user's attributes whose id corresponds
        to the id provided to the function"""
        user = self.find_user_by(id=user_id)
        valid_attributes = ['email', 'hashed_password', 'session_id',
                            'reset_token']
        invalid_attributes = [attr for attr in valid_attributes if not
                              hasattr(user, attr)]

        if invalid_attributes:
            raise ValueError

        for attr, value in kwargs.items():
            if attr in valid_attributes:
                setattr(user, attr, value)

        self._session.commit()
        return None
