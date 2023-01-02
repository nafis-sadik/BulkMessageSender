from fastapi import APIRouter

from Models.ViewModels.RobotModelVM import RobotsModelVM
from Services.Abstractions.IRobotSettingsService import IRobotSettingsService
from Services.Implementations.RobotSettingsService import RobotSettingsService

robot_module = APIRouter(
    prefix='/robots',
    tags=["Robot Settings"],
    responses={
        500: {"description": "Internal Error"},
        404: {"description": "Not found"},
        200: {"description": "OK"}
    }
)


@robot_module.post('')
async def add_robot(robot_model: RobotsModelVM):
    robot_service: IRobotSettingsService = RobotSettingsService()
    return await robot_service.add_async(robot_model)


@robot_module.put('')
async def update_robot(robot_model: RobotsModelVM):
    robot_service: IRobotSettingsService = RobotSettingsService()
    return await robot_service.update_async(robot_model)


@robot_module.get('/{robot_id}')
async def get_robot_by_id(robot_id: int):
    robot_service: IRobotSettingsService = RobotSettingsService()
    return await robot_service.get_robot_async(robot_id)


@robot_module.get('/GetAllAsync/')
async def get_robots():
    robot_service: IRobotSettingsService = RobotSettingsService()
    return await robot_service.get_all_robots_async()


@robot_module.delete('/{robot_id}')
async def remove(robot_id: int):
    robot_service: IRobotSettingsService = RobotSettingsService()
    return await robot_service.delete_async(robot_id)
