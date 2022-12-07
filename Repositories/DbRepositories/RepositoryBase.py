import os
from abc import ABC

import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy_utils import create_database
from sqlalchemy_utils.functions import database_exists

from Repositories.DbRepositories.IRepositoryBase import IRepositoryBase


class RepositoryBase(IRepositoryBase, ABC):
    def __init__(self, entity: type):
        self.engine = create_engine(os.getenv('CONNECTION_STRING_SQLITE'), echo=False)

        if database_exists(os.getenv('CONNECTION_STRING_SQLITE')) is not True:
            # create_database(os.getenv('CONNECTION_STRING_SQLITE'))
            metadata = sqlalchemy.MetaData()
            metadata.create_all(self.engine, checkfirst=True)

        session_maker: sessionmaker = sessionmaker(bind=self.engine)
        self.session: Session = session_maker()
        self.engine.scalar()
        self.entity_type = entity

    async def get_version(self):
        return await sqlalchemy.__version__

    async def add(self, data):
        return await self.session.add(data)

    async def delete(self, data):
        await self.session.delete(data)

    async def commit(self):
        await self.session.commit()

    async def get_count(self) -> int:
        return await self.session.query(self.entity_type).count()

    async def get(self, *args) -> list:
        return await self.session.query(self.entity_type).filter(*args).all()

    async def get_first(self, *args):
        return await self.session.query(self.entity_type).filter(*args).one()

    async def get_all(self) -> list:
        return await self.session.query(self.entity_type).all()

    async def get_col(self, **arguments) -> list:
        return await self.session.query(arguments['cols']).filter(arguments['conditions']).all()

    async def max(self, col_map) -> int:
        return await self.session.query(func.max(col_map)).scalar()

    def __del__(self):
        await self.session.close()
