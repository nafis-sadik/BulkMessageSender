import glob
import os

from fastapi import APIRouter

from WebApplication.Controllers.CampaignsController import campaign_module
from WebApplication.Controllers.ContactFileController import csv_module
from WebApplication.Controllers.ContactsController import contacts_module
from WebApplication.Controllers.RobotControlCenterController import robot_control_center_module
from WebApplication.Controllers.RobotController import robot_module

router = APIRouter()
router.include_router(robot_module)
router.include_router(robot_control_center_module)
router.include_router(contacts_module)
router.include_router(campaign_module)
router.include_router(csv_module)

__all__ = [os.path.basename(file_path)[:-3] for file_path in glob.glob(os.path.dirname(__file__) + "/*.py")]
