from fastapi import APIRouter

from Repositories.SeliniumRepositories.ChromeService import ChromeService
from Services.WhatsappRobotService import WhatsappRobotService

whatsapp_robot = APIRouter(
    prefix='/api',
    tags=["Whatsapp Bulk MMS Bot"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"}
    }
)


@whatsapp_robot.get('/StartRobot/{robot_id}')
async def start_robot(robot_id: int):
    browser_service: ChromeService = ChromeService()
    browser_user: str = 'Election'
    service: WhatsappRobotService = WhatsappRobotService(browser_service, browser_user)
    service.new_window()
    return 'Success'


@whatsapp_robot.get('/StopRobot')
async def stop_robot():
    raise NotImplementedError("Under Development")


@whatsapp_robot.get('/DeleteRobot')
async def delete_robot():
    raise NotImplementedError("Under Development")


@whatsapp_robot.get('/ListRobots')
async def get_all_robot():
    raise NotImplementedError("Under Development")
