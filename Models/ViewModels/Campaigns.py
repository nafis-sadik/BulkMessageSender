from datetime import datetime

from pydantic import Field
from pydantic.main import BaseModel


class CampaignVM(BaseModel):
    campaign_id: int = Field(None, title='Campaign Id')
    campaign_name: str = Field(None, title='Campaign Name')
    content_text: str = Field(None, title='Campaign Text')
    content_media: str = Field(None, title='Campaign Media Path')
    date: datetime = Field(None, title='Campaign Start Date')
