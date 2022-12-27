from abc import ABC

from JobHandelers.Abstractions.IContactsJob import IContactsJob


class ContactsJob(IContactsJob, ABC):
    async def sync_contacts(self, file_path: str) -> None:
        file_path = 'Contacts.csv'
        print(f'/static/{file_path}')
