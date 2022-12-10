import glob
import os

from fastapi import APIRouter

from WebApplication.Controllers.AppSettingsController import app_settings
from WebApplication.Controllers.RobotController import robot_module
from WebApplication.Controllers.WhatsappController import whatsapp_robot

router = APIRouter()
router.include_router(whatsapp_robot)
router.include_router(robot_module)
router.include_router(app_settings)

__all__ = [os.path.basename(file_path)[:-3] for file_path in glob.glob(os.path.dirname(__file__) + "/*.py")]
