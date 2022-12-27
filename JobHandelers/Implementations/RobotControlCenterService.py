import threading
from abc import ABC
from typing import Optional

from Models.LookupValues.LookupValues import Platforms, Browsers
from Models.ViewModels.RobotModel import RobotsModel
from Repositories.SeliniumRepositories.ChromeService import ChromeService
from Repositories.SeliniumRepositories.IBrowserService import IBrowserService
from JobHandelers.Abstractions.IRobotControlCenterService import IRobotControlCenterService
from Services.Abstractions.IRobotOperationsService import IRobotOperationsService
from Services.Abstractions.IRobotSettingsService import IRobotSettingsService
from Services.Implementations.RobotSettingsService import RobotSettingsService
from Services.Implementations.WhatsappBulkMediaBot import WhatsappBulkVideoBot


class RobotControlCenterService(IRobotControlCenterService, ABC):
    __instance = None  # Holds reference to an object of this class

    @staticmethod
    def initialize():
        """ Static access method. """
        if RobotControlCenterService.__instance is None:
            RobotControlCenterService.__instance = RobotControlCenterService()
        return RobotControlCenterService.__instance

    def __init__(self):
        self.robot_pool = {}
        if RobotControlCenterService.__instance is not None:
            raise Exception('Singleton instance already exists')
        else:
            RobotControlCenterService.__instance = self

    async def initialize_robot(self, robot_id: int) -> None:
        bot_settings_service: IRobotSettingsService = RobotSettingsService()
        robot_model: RobotsModel = await bot_settings_service.get_robot_async(robot_id)

        if robot_model.is_deleted:
            raise Exception(f'Robot name {robot_model.robot_name} is unavailable')

        # Browser selection for robot
        browser_service: IBrowserService
        if robot_model.browser_selection == Browsers.Chrome:
            browser_service = ChromeService()
        else:
            raise Exception(f'Unsupported browser {robot_model.browser_selection}')

        # Platform selection for robot
        robot: IRobotOperationsService
        if robot_model.platform_selection == Platforms.Whatsapp:
            robot = WhatsappBulkVideoBot(browser_service, robot_model)
        else:
            raise Exception(f'Unsupported platform {robot_model.platform_selection}')

        # Keep the robot in the robot pool so that the GC don't take it away and the robot could be easily and
        # uniquely be identified to control
        self.robot_pool[robot_model.robot_name] = robot

    async def start_robot(self, robot_id: int) -> None:
        bot_settings_service: IRobotSettingsService = RobotSettingsService()
        robot_model: RobotsModel = await bot_settings_service.get_robot_async(robot_id)

        if robot_model.is_deleted:
            raise Exception(f'Robot name {robot_model.robot_name} is unavailable')

        # Get the robot from the pool
        if robot_model.robot_name in self.robot_pool.keys():
            robot: IRobotOperationsService = self.robot_pool[robot_model.robot_name]
            new_robot_thread = threading.Thread(target=robot.start)
            new_robot_thread.start()
        else:
            raise Exception(f'Robot {robot_model.robot_name} is not initialized')

    async def stop_robot(self, robot_id: int) -> None:
        bot_settings_service: IRobotSettingsService = RobotSettingsService()
        robot_model: RobotsModel = await bot_settings_service.get_robot_async(robot_id)

        if robot_model.is_deleted:
            raise Exception(f'Robot name {robot_model.robot_name} is unavailable')

        # Get the robot from the pool
        if robot_model.robot_name in self.robot_pool.keys():
            robot: IRobotOperationsService = self.robot_pool[robot_model.robot_name]
            robot.stop()
        else:
            raise Exception(f'Robot {robot_model.robot_name} is not initialized')

    async def terminate_robot(self, robot_id: int) -> None:
        bot_settings_service: IRobotSettingsService = RobotSettingsService()
        robot_model: RobotsModel = await bot_settings_service.get_robot_async(robot_id)

        if robot_model.is_deleted:
            raise Exception(f'Robot name {robot_model.robot_name} is unavailable')

        # Get the robot from the pool
        if robot_model.robot_name in self.robot_pool.keys():
            robot: IRobotOperationsService = self.robot_pool[robot_model.robot_name]
            robot.terminate()
            self.robot_pool.pop(robot_model.robot_name)
        else:
            raise Exception(f'Robot {robot_model.robot_name} is not initialized')

    def get_all_alive_robots(self) -> list:
        return list(self.robot_pool.keys())

    async def get_robot(self, robot_id: int) -> Optional[IRobotOperationsService]:
        bot_settings_service: IRobotSettingsService = RobotSettingsService()
        robot_model: RobotsModel = await bot_settings_service.get_robot_async(robot_id)

        if robot_model.is_deleted:
            raise Exception(f'Robot name {robot_model.robot_name} is unavailable')

        if robot_model.robot_name in self.robot_pool.keys():
            return self.robot_pool[robot_model.robot_name]
        else:
            raise Exception(f'Robot {robot_model.robot_name} is not initialized')
