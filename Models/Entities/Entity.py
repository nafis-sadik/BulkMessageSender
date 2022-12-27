import os

import sqlalchemy
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Robots(Base):
    __tablename__ = 'Robots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    robot_name = Column(String)
    platform_selection = Column(String)
    browser_selection = Column(String)
    is_incognito = Column(Boolean)
    is_headless = Column(Boolean)
    is_deleted = Column(Boolean)


class Locations(Base):
    __tablename__ = 'Locations'

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String)


class Campaigns(Base):
    __tablename__ = 'Campaigns'
    campaign_id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_name = Column(String, nullable=False)
    content_text = Column(String)
    content_media = Column(String)
    date = Column(DateTime)


class CampaignHistory(Base):
    __tablename__ = 'CampaignHistory'

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(Integer, nullable=False)
    contact_id = Column(Integer, nullable=False)
    campaign_relation = relationship("Campaigns")
    contacts_relation = relationship("Contacts")


class Contacts(Base):
    __tablename__ = 'Contacts'

    contact_id = Column(Integer, primary_key=True, autoincrement=True)
    contact_number = Column(Integer, nullable=False)
    location_id = Column(Integer)
    locations_relation = relationship("Locations")


class ContactsFiles(Base):
    __tablename__ = 'ContactsFiles'

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    file_path = Column(String)
    original_file_name = Column(String)


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    DATABASE_URL = os.getenv('CONNECTION_SQLITE')

    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

    metadata = sqlalchemy.MetaData()
    Base.metadata.create_all(engine, checkfirst=True)
