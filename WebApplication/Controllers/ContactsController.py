import os

from fastapi import APIRouter

from JobHandelers.Implementations.ContactsJob import ContactsJob

contacts_module = APIRouter(
    prefix='/contacts',
    tags=["Contact Manager"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"},
        500: {"description": "Internal Error"}
    }
)


@contacts_module.delete('files/{file_id}')
async def delete_file(file_id: int):
    return {"Result": file_id}
