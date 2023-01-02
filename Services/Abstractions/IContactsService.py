from Models.ViewModels.ContactsVM import ContactsVM
from Models.ViewModels.PaginationModel import PaginationModel


class IContactsService:
    async def save_contacts(self, contacts: list):
        raise NotImplementedError

    async def save_contact(self, contacts: ContactsVM):
        raise NotImplementedError

    async def delete_contact(self, contacts: ContactsVM):
        raise NotImplementedError

    async def get_contacts(self, pagination: PaginationModel):
        raise NotImplementedError
