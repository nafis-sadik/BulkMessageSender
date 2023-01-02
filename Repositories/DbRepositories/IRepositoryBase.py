from Models.ViewModels.PaginationModel import PaginationModel


class IRepositoryBase:
    async def get_version(self):
        raise NotImplementedError

    def add(self, data: any) -> None:
        raise NotImplementedError

    def delete(self, data: any) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError

    async def get_list(self, *args) -> list:
        raise NotImplementedError

    async def get(self, *args):
        raise NotImplementedError

    async def get_count(self) -> int:
        raise NotImplementedError

    async def get_paged_list(self, paging_data: PaginationModel) -> PaginationModel:
        raise NotImplementedError

    async def max(self, col_map):
        raise NotImplementedError
