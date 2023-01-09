import logging
import platform
from abc import ABC

from automapper import mapper

from Models.Entities.Entity import Contacts
from Models.ViewModels.ContactsVM import ContactsVM
from Models.ViewModels.PaginationModel import PaginationModel
from Repositories.DbRepositories.IRepositoryBase import IRepositoryBase
from Repositories.DbRepositories.RepositoryBase import RepositoryBase
from Services.Abstractions.IContactsService import IContactsService


class ContactsService(IContactsService, ABC):
    def __init__(self):
        self.contacts_repo: IRepositoryBase = RepositoryBase(Contacts)
        self.logger = logging.getLogger('ServerLog')

    async def save_contacts(self, contacts: list):
        try:
            for contact in contacts:
                if await self.contacts_repo.get(contact == Contacts.contact_number):
                    print(f'{contact} is already saved')
                    continue

                self.contacts_repo.add(Contacts(
                    contact_number=contact,
                    booking_status=False
                ))
            await self.contacts_repo.commit()
        except Exception as ex:
            await self.contacts_repo.rollback()
            details = {'platform': platform.node(), 'target': 'save_contacts'}
            self.logger.error('Whatsapp Bulk Video Bot Service: %s', str(ex), extra=details)

    async def save_contact(self, contact: ContactsVM):
        try:
            if await self.contacts_repo.get(contact.contact_number == Contacts.contact_number):
                raise Exception(f'{contact.contact_number} is already saved')

            contact_entity = mapper.to(Contacts).map(contact)
            contact_entity.booking_status = False
            self.contacts_repo.add(contact_entity)
            await self.contacts_repo.commit()
        except Exception as ex:
            await self.contacts_repo.rollback()
            details = {'platform': platform.node(), 'target': 'save_contact'}
            self.logger.error('Whatsapp Bulk Video Bot Service: %s', str(ex), extra=details)

    async def delete_contact(self, contact: ContactsVM):
        try:
            if await self.contacts_repo.get(contact.contact_number == Contacts.contact_number) is None:
                raise Exception(f'{contact.contact_number} is not saved')

            contact_entity = mapper.to(Contacts).map(contact)
            self.contacts_repo.delete(contact_entity)
            await self.contacts_repo.commit()
        except Exception as ex:
            await self.contacts_repo.rollback()
            details = {'platform': platform.node(), 'target': 'delete_contact'}
            self.logger.error('Whatsapp Bulk Video Bot Service: %s', str(ex), extra=details)

    async def get_contacts(self, pagination: PaginationModel):
        try:
            return await self.contacts_repo.get_paged_list(pagination)
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'get_contacts'}
            self.logger.error('Whatsapp Bulk Video Bot Service: %s', str(ex), extra=details)
