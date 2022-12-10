import os
from abc import ABC

import sqlalchemy
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils.functions import database_exists

from Repositories.DbRepositories.IRepositoryBase import IRepositoryBase


class RepositoryBase(IRepositoryBase, ABC):
    def __init__(self, entity: type):
        self.engine = create_async_engine(os.getenv('CONNECTION_SQLITE_ASYNC'), echo=False)

        if database_exists(os.getenv('CONNECTION_SQLITE_ASYNC')) is not True:
            create_database(os.getenv('CONNECTION_SQLITE_ASYNC'))
            metadata = sqlalchemy.MetaData()
            metadata.create_all(self.engine, checkfirst=True)

        session_maker: sessionmaker = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        self.session: Session = session_maker()
        self.entity_type = entity

    async def get_version(self):
        return await sqlalchemy.__version__

    def add(self, data):
        self.session.add(data)

    def delete(self, data):
        self.session.delete(data)

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()
        await self.session.flush()
        await self.session.close()
        await self.engine.dispose()

    async def get_count(self) -> int:
        return await self.session.query(self.entity_type).count()

    async def get(self, *args):
        query = await self.session.execute(select(self.entity_type).where(*args))
        return query.scalar()

    async def get_list(self, *args) -> list:
        query = await self.session.execute(select(self.entity_type).where(*args))
        return query.scalars().all()

    async def max(self, col_map):
        return await self.session.execute(select(self.entity_type).where(func.max(col_map))).scalar()
