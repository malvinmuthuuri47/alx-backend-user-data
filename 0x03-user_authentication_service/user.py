#!/usr/bin/env python3
"""User model"""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from typing import Optional

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class User(Base):
    """This class defines the structure of a user model for a Database
    using SQLAlchemy with various attributes that can be stored in a
    database"""
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: Optional[str] = Column(String(250))
    reset_token: Optional[str] = Column(String(250))
