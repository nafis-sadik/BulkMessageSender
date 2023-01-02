from fastapi import APIRouter

from JobHandelers.Abstractions.IRobotControlCenterService import IRobotControlCenterService
from JobHandelers.Implementations.RobotControlCenterService import RobotControlCenterService

robot_control_center_module = APIRouter(
    prefix='/controls',
    tags=["Robot Control Center"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"}
    }
)


@robot_control_center_module.get('/initialize/{robot_id}')
async def initialize_robot(robot_id: int):
    robot_control_service: IRobotControlCenterService = RobotControlCenterService.initialize()
    return await robot_control_service.initialize_robot(robot_id=robot_id)


@robot_control_center_module.get('/start/{robot_id}')
async def start_robot(robot_id: int):
    robot_control_service: IRobotControlCenterService = RobotControlCenterService.initialize()
    return await robot_control_service.start_robot(robot_id=robot_id)


@robot_control_center_module.get('/stop/{robot_id}')
async def stop_robot(robot_id: int):
    robot_control_service: IRobotControlCenterService = RobotControlCenterService.initialize()
    return await robot_control_service.stop_robot(robot_id=robot_id)


@robot_control_center_module.get('/terminate/{robot_id}')
async def terminate_robot(robot_id: int):
    robot_control_service: IRobotControlCenterService = RobotControlCenterService.initialize()
    return await robot_control_service.terminate_robot(robot_id=robot_id)


@robot_control_center_module.get('/{robot_id}')
async def get_robots(robot_id: int):
    robot_control_service: IRobotControlCenterService = RobotControlCenterService.initialize()
    return await robot_control_service.get_robot(robot_id=robot_id)


@robot_control_center_module.get('/GetAllAsync/')
async def get_robots_online():
    robot_control_service: IRobotControlCenterService = RobotControlCenterService.initialize()
    return robot_control_service.get_all_alive_robots()
