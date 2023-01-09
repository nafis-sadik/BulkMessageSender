import os
import threading
from datetime import datetime

import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException

from JobHandelers.Implementations.ContactsJob import ContactsJob
from Models.ViewModels.PaginationModel import PaginationModel
from Services.Abstractions.IContactsFilesService import IContactsFilesService
from Services.Implementations.ContactsFilesService import ContactsFilesService

special_characters = ['@', '#', '$', '*', '&', ' ']

csv_module = APIRouter(
    prefix='/csv',
    tags=["CSV File Manager"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"},
        500: {"description": "Internal Error"}
    }
)


@csv_module.get('/storage/')
async def get_files():
    return os.listdir('./contacts_files/')


@csv_module.post('/pagination/')
async def get_file_list(paging_data: PaginationModel):
    try:
        contacts_service: IContactsFilesService = ContactsFilesService()
        return await contacts_service.get_file_list(paging_data)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@csv_module.delete('/')
async def delete_file(file_id: int):
    try:
        contacts_service: IContactsFilesService = ContactsFilesService()
        contacts_service.remove_file(file_id)
        return {"Result": "OK"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@csv_module.post('/')
async def upload_file(file: UploadFile = File(description=".csv file of contact numbers")):
    try:
        file_name: str = file.filename

        for ch in special_characters:
            file_name = file_name.replace(ch, "_")

        time_stamp = datetime.timestamp(datetime.now())
        file_name = str(time_stamp) + '_' + file_name

        destination_file_path = './contacts_files/' + file_name  # location to store file
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await file.read(1024):  # async read file chunk
                await out_file.write(content)  # async write file chunk

        contacts_service: IContactsFilesService = ContactsFilesService()
        await contacts_service.add_file(file_name, file.filename, destination_file_path)
        return {"Result": "OK"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@csv_module.get('/sync/{file_id}')
async def sync_file(file_id: int):
    contact_file_job: ContactsJob = ContactsJob()
    robot_thread = threading.Thread(target=contact_file_job.sync_contacts, args=(file_id,))
    robot_thread.start()
    return {'Result': 'Successful'}
