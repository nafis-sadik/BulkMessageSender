from pydantic.fields import Field
from pydantic.main import BaseModel


class RobotsModel(BaseModel):
    id: int = Field(None, title='Robot Id')
    robot_name: str = Field(None, title='Robot Name', max_length=100)
    platform_selection: str = Field(None, title='Select Messaging Service', max_length=100)
    browser_selection: str = Field(None, title='Select Browser for Robot', max_length=100)
    is_incognito: bool = Field(None, title='Should the Robot use Incognito Mode')
    is_headless: bool = Field(None, title='Should the Robot use the Browser in Headless Mode?')
