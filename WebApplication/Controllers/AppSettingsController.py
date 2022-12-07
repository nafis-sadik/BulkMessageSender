from fastapi import APIRouter

from Repositories.SeliniumRepositories.ChromeService import ChromeService
from Services.WhatsappRobotService import WhatsappRobotService

app_settings = APIRouter(
    prefix='/api',
    tags=["Application Settings"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"}
    }
)


@app_settings.get('/StartRobot')
async def save_settings():
    browser_service: ChromeService = ChromeService()
    browser_user: str = 'Election'
    service: WhatsappRobotService = WhatsappRobotService(browser_service, browser_user)
    service.new_window()
    return 'Success'
