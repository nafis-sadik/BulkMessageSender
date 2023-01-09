import logging
import platform
from abc import ABC

from automapper import mapper

from Models.Entities.Entity import ContactsFiles
from Models.ViewModels.ContactsFileVM import ContactsFileVM
from Models.ViewModels.PaginationModel import PaginationModel
from Repositories.DbRepositories.IRepositoryBase import IRepositoryBase
from Repositories.DbRepositories.RepositoryBase import RepositoryBase
from Services.Abstractions.IContactsFilesService import IContactsFilesService


class ContactsFilesService(IContactsFilesService, ABC):
    def __init__(self):
        self.contact_files_repo: IRepositoryBase = RepositoryBase(ContactsFiles)
        self.logger = logging.getLogger('ServerLog')

    async def add_file(self, saved_file_name: str, file_name: str, file_path: str):
        try:
            self.contact_files_repo.add(ContactsFiles(
                file_name=saved_file_name,
                file_path=file_path,
                original_file_name=saved_file_name
            ))

            await self.contact_files_repo.commit()
            return True
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'save_file'}
            self.logger.error('Contacts Files Service: %s', str(ex), extra=details)

    async def update_file_info(self, view_model: ContactsFileVM):
        try:
            file_entity: ContactsFiles = await self.contact_files_repo.get(ContactsFiles.file_id == view_model.file_id)

            file_entity.file_name = view_model.file_name
            file_entity.file_path = view_model.file_path
            file_entity.file_sync_status = view_model.file_sync_status

            await self.contact_files_repo.commit()
            return True
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'update_file_info'}
            self.logger.error('Contacts Files Service: %s', str(ex), extra=details)

    def remove_file(self, file_id: int):
        try:
            contacts_files = self.contact_files_repo.get(ContactsFiles.file_id == file_id)
            if contacts_files is not None:
                self.contact_files_repo.add(contacts_files)
            else:
                raise Exception('File not found')
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'save_file'}
            self.logger.error('Contacts Files Service: %s', str(ex), extra=details)

    async def get_file_list(self, paging_data: PaginationModel) -> PaginationModel:
        try:
            contacts_files: PaginationModel = await self.contact_files_repo.get_paged_list(paging_data)
            file_list_model = list()

            for file_model in contacts_files.data_collection:
                view_model = mapper.to(ContactsFileVM).map(file_model)
                file_list_model.append(view_model)

            contacts_files.data_collection = file_list_model
            return contacts_files
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'save_file'}
            self.logger.error('Contacts Files Service: %s', str(ex), extra=details)

    async def get_file(self, file_id: int) -> ContactsFileVM:
        try:
            file_entity: ContactsFiles = await self.contact_files_repo.get(ContactsFiles.file_id == file_id)
            view_model = mapper.to(ContactsFileVM).map(file_entity)
            return view_model
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'get_file'}
            self.logger.error('Contacts Files Service: %s', str(ex), extra=details)
