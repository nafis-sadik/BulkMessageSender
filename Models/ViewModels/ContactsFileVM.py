from pydantic import Field
from pydantic.main import BaseModel


class ContactsFileVM(BaseModel):
    file_id: int = Field(None, title='File Id')
    file_name: str = Field(None, title='File Name')
    file_path: str = Field(None, title='File Path')
    file_sync_status: str = Field(None, title='Sync Status')
    original_file_name: str = Field(None, title='Upload name of file')
