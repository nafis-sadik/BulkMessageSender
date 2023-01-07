from pydantic import Field


class ContactsFileVM:
    file_id: int = Field(None, title='File Id')
    file_name: str = Field(None, title='File Name')
    file_path: str = Field(None, title='File Path')
    file_sync_status: str = Field(None, title='Sync Status')
    original_file_name: str = Field(None, title='Upload name of file')

    @staticmethod
    def get_fields(cls):
        return ['file_id', 'file_name', 'file_path', 'original_file_name']
