class IRepositoryBase:
    async def get_version(self):
        raise NotImplementedError

    async def add(self, data: any) -> None:
        raise NotImplementedError

    async def delete(self, data: any) -> None:
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError

    async def get_first(self, *args):
        raise NotImplementedError

    async def get_all(self) -> list:
        raise NotImplementedError

    async def get_col(self, *conditions, **cols) -> list:
        raise NotImplementedError

    async def get(self, *args) -> list:
        raise NotImplementedError

    async def get_count(self) -> int:
        raise NotImplementedError

    async def max(self, col_map) -> int:
        raise NotImplementedError
