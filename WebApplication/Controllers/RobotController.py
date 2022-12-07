from fastapi import APIRouter

from Models.ViewModels.RobotModel import RobotsModel
from Services.Abstractions.IRobotSettingsService import IRobotSettingsService
from Services.Implementations.RobotSettingsService import RobotSettingsService

robot_module = APIRouter(
    prefix='/api',
    tags=["Robot Settings"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"}
    }
)


@robot_module.post('/AddRobot')
async def add_robot(robot_model: RobotsModel):
    robot_service: IRobotSettingsService = RobotSettingsService()
    return await robot_service.add_async(robot_model)


@robot_module.post('/UpdateRobot')
async def update_robot(robot_model: RobotsModel):
    robot_service: IRobotSettingsService = RobotSettingsService()
    return await robot_service.update_async(robot_model)


@robot_module.get('/GetRobotByIdAsync/{robot_id}')
async def get_robot_by_id(robot_id: int):
    robot_service: IRobotSettingsService = RobotSettingsService()
    return await robot_service.get_robot_async(robot_id)


@robot_module.get('/GetAllRobotsAsync')
async def get_robot_by_id():
    robot_service: IRobotSettingsService = RobotSettingsService()
    return await robot_service.get_all_robots_async()
