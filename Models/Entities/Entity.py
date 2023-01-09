import asyncio
import os

import sqlalchemy
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class LookUpTable(Base):
    __tablename__ = 'LookUpTable'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String)
    field = Column(String)
    lookup_display_text = Column(String)


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


class Contacts(Base):
    __tablename__ = 'Contacts'

    contact_id = Column(Integer, primary_key=True, autoincrement=True)
    contact_number = Column(Integer, nullable=False)
    location_id = Column(Integer, ForeignKey('Locations.location_id'))
    booking_status = Column(Boolean, nullable=False)
    locations_relation = relationship(
        "Locations",
        primaryjoin="(Contacts.location_id==Locations.location_id)",
        foreign_keys=Locations.location_id
    )


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
    campaign_id = Column(Integer, ForeignKey('Campaigns.campaign_id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('Contacts.contact_id'), nullable=False)
    campaign_relation = relationship(
        "Campaigns",
        primaryjoin="(CampaignHistory.campaign_id==Campaigns.campaign_id)",
        foreign_keys=Campaigns.campaign_id
    )
    contacts_relation = relationship(
        "Contacts",
        primaryjoin="(CampaignHistory.contact_id==Contacts.contact_id)",
        foreign_keys=Contacts.contact_id
    )


class ContactsFiles(Base):
    __tablename__ = 'ContactsFiles'

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    file_path = Column(String)
    original_file_name = Column(String)
    file_sync_status = Column(Integer)

    contacts_relation = relationship(
        "LookUpTable",
        primaryjoin="(ContactsFiles.file_sync_status==LookUpTable.id)",
        foreign_keys=LookUpTable.id
    )


async def load_data(async_engine):
    async_session = sessionmaker(async_engine, expire_on_commit=True, class_=AsyncSession)

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    LookUpTable(
                        table_name='ContactsFiles',
                        field='file_sync_status',
                        lookup_display_text='Not Synced'
                    ),
                    LookUpTable(
                        table_name='ContactsFiles',
                        field='file_sync_status',
                        lookup_display_text='Syncing'
                    ),
                    LookUpTable(
                        table_name='ContactsFiles',
                        field='file_sync_status',
                        lookup_display_text='Synced'
                    ),
                    LookUpTable(
                        table_name='Robots',
                        field='platform_selection',
                        lookup_display_text='Whatsapp'
                    ),
                    LookUpTable(
                        table_name='Robots',
                        field='browser_selection',
                        lookup_display_text='Chrome'
                    ),
                    Robots(
                        id=1,
                        robot_name='Whatsapp Bulk Bot 1',
                        platform_selection='Whatsapp',
                        browser_selection='Chrome',
                        is_incognito=True,
                        is_deleted=False,
                        is_headless=False
                    ),
                    Robots(
                        id=2,
                        robot_name='Whatsapp Bulk Bot 2',
                        platform_selection='Whatsapp',
                        browser_selection='Chrome',
                        is_incognito=True,
                        is_deleted=False,
                        is_headless=False
                    ),
                    Robots(
                        id=3,
                        robot_name='Whatsapp Bulk Bot 3',
                        platform_selection='Whatsapp',
                        browser_selection='Chrome',
                        is_incognito=True,
                        is_deleted=False,
                        is_headless=False
                    ),
                    ContactsFiles(
                        file_id=1,
                        file_name='1672481245.431586_Book_3.csv',
                        file_path='./contacts_files/1672481245.431586_Book_3.csv',
                        original_file_name='Book 3.csv',
                        file_sync_status=1
                    )
                ]
            )

        await session.commit()


async def init(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    DATABASE_URL = os.getenv('CONNECTION_SQLITE')

    # engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
    engine = create_async_engine(DATABASE_URL, echo=True)

    metadata = sqlalchemy.MetaData()

    asyncio.run(init(engine))
    asyncio.run(load_data(engine))
