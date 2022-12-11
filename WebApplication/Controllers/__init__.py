import glob
import os

from fastapi import APIRouter

from WebApplication.Controllers.RobotControlCenterController import robot_control_center_module
from WebApplication.Controllers.RobotController import robot_module

router = APIRouter()
router.include_router(robot_module)
router.include_router(robot_control_center_module)

__all__ = [os.path.basename(file_path)[:-3] for file_path in glob.glob(os.path.dirname(__file__) + "/*.py")]
