# import asyncio
import os
from abc import ABC
import sqlalchemy.dialects.sqlite
import sqlalchemy
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from Models.ViewModels.PaginationModel import PaginationModel
from Repositories.DbRepositories.IRepositoryBase import IRepositoryBase


class RepositoryBase(IRepositoryBase, ABC):
    def __init__(self, entity: type):
        self.entity_type = entity
        conn_str: str = os.getenv('CONNECTION_SQLITE_ASYNC')
        self.async_engine = create_async_engine(conn_str, echo=False)

        session_maker: sessionmaker = sessionmaker(self.async_engine, expire_on_commit=False, class_=AsyncSession)
        self.session: AsyncSession = session_maker()

    async def get_version(self):
        return sqlalchemy.__version__

    def add(self, data):
        self.session.add(data)

    def delete(self, data):
        self.session.delete(data)

    async def get_count(self) -> int:
        return await self.session.execute(select(self.entity_type).count())

    async def get_paged_list(self, paging_data: PaginationModel) -> PaginationModel:
        result = await self.session \
            .execute(select(self.entity_type)
                     .offset(paging_data.page_length * (paging_data.page_number - 1))
                     .limit(paging_data.page_length))
        paging_data.data_collection = result.scalars().all()
        return paging_data

    async def get(self, *args):
        result = await self.session.execute(select(self.entity_type).where(*args))
        return result.scalars().first()

    async def get_list(self, *args) -> list:
        result = await self.session.execute(select(self.entity_type).where(*args))
        return result.scalars().all()

    async def max(self, col_map):
        result = await self.session.execute(select(self.entity_type).where(func.max(col_map)))
        return result

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()

    async def close(self):
        await self.session.flush()
        await self.session.close()
        await self.async_engine.dispose()

    # async def __aenter__(self):
    #     raise NotImplementedError
    #
    # async def __aexit__(self):
    #     await self.session.flush()
    #     await self.session.close()
    #     await self.async_engine.dispose()
    #
    # def __del__(self):
    #     asyncio.run(self.session.flush())
    #     asyncio.run(self.session.close())
    #     asyncio.run(self.async_engine.dispose())
