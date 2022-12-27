import os
from datetime import datetime

import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException

contacts_module = APIRouter(
    prefix='/contacts',
    tags=["Contact Manager"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"},
        500: {"description": "Internal Error"}
    }
)

special_characters = ['@', '#', '$', '*', '&', ' ']


@contacts_module.get('files')
async def get_files():
    return os.listdir('./contacts_files/')


@contacts_module.post('/upload')
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

        return {"Result": "OK"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
