import csv
from abc import ABC

from JobHandelers.Abstractions.IContactsJob import IContactsJob
from Models.ViewModels.ContactsFileVM import ContactsFileVM
from Services.Abstractions.IContactsFilesService import IContactsFilesService
from Services.Abstractions.IContactsService import IContactsService
from Services.Implementations.ContactsFilesService import ContactsFilesService
from Services.Implementations.ContactsService import ContactsService


class ContactsJob(IContactsJob, ABC):

    async def sync_contacts(self, file_id: int) -> None:
        contacts_file_service: IContactsFilesService = ContactsFilesService()
        file_details: ContactsFileVM = await contacts_file_service.get_file(file_id)
        file_details.file_sync_status = 2
        await contacts_file_service.update_file_info(file_details)

        contact_list: list = ContactsJob.read_csv(file_details.file_path)
        contacts_service: IContactsService = ContactsService()
        contacts_service.save_contacts(contact_list)

        file_details.file_sync_status = 3
        await contacts_file_service.update_file_info(file_details)

    @classmethod
    def read_csv(cls, file_path):
        number_collection: list = list()
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in csv_reader:
                number_collection.append(row[0])
        return number_collection
