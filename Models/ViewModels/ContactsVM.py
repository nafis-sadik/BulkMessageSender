from pydantic.fields import Field
from pydantic.main import BaseModel


class ContactsVM(BaseModel):
    contact_id: int = Field(None, title='Contact Id')
    contact_number: int = Field(None, title='Contact Number')
    location_id: int = Field(None, title='Location Id')
