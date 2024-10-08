#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from typing import TypeVar


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
        """add a user object to db"""
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            user = None
            self._session.rollback()
        return user

    def find_user_by(self, **kwargs) -> User:
        """finds a user in db"""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id, **kwargs) -> None:
        """used to update a user"""
        try:
            user = self.find_user_by(id=user_id)
            for k, v in kwargs.items():
                if not hasattr(user, k):
                    raise ValueError
                setattr(user, k, v)
            self._session.commit()
        except ValueError as e:
            self._session.rollback()
            raise e
        except NoResultFound as e:
            self._session.rollback()
            raise e
        except InvalidRequestError as e:
            self._session.rollback()
            raise e
