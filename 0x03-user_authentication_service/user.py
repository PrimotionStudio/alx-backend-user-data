#!/usr/bin/env python3
"""
create a SQLAlchemy model named User
for a database table named users
(by using the mapping declaration of SQLAlchemy).

The model will have the following attributes:

id, the integer primary key
email, a non-nullable string
hashed_password, a non-nullable string
session_id, a nullable string
reset_token, a nullable string
"""
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# database_url = "mysql://localhost:3306/db"
# engine = create_engine(database_url)
Base = declarative_base()


class User(Base):
    """
    Class Model for the users table
    """
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    email = Column("email", VARCHAR(250), nullable=False)
    hashed_password = Column("hashed_password", VARCHAR(250), nullable=False)
    session_id = Column("session_id", VARCHAR(250), nullable=True)
    reset_token = Column("reset_token", VARCHAR(250), nullable=True)
