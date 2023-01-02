from pydantic.fields import Field
from pydantic.main import BaseModel


class PaginationModel(BaseModel):
    page_number: int = Field(None, title='Page Number')
    page_length: int = Field(None, title='Page Length')
    page_count: int = Field(None, title='Page Count')
    data_collection: list = Field(None, title="Data")

