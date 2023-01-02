from Models.ViewModels.ContactsFileVM import ContactsFileVM
from Models.ViewModels.PaginationModel import PaginationModel


class IContactsFilesService:
    async def add_file(self, saved_file_name: str, file_name: str, file_path: str):
        raise NotImplementedError

    async def update_file_info(self, view_model: ContactsFileVM):
        raise NotImplementedError

    def remove_file(self, file_id: int):
        raise NotImplementedError

    async def get_file_list(self, paging_data: PaginationModel) -> PaginationModel:
        raise NotImplementedError

    async def get_file(self, file_id: int) -> ContactsFileVM:
        raise NotImplementedError
