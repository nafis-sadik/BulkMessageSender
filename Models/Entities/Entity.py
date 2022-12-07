import os

import sqlalchemy
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Robots(Base):
    __tablename__ = 'Robots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_name = Column(String)
    platform_selection = Column(String)
    browser_selection = Column(String)
    is_incognito = Column(Boolean)
    is_headless = Column(Boolean)


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    DATABASE_URL = os.getenv('CONNECTION_STRING_SQLITE')

    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

    metadata = sqlalchemy.MetaData()
    Base.metadata.create_all(engine, checkfirst=True)
