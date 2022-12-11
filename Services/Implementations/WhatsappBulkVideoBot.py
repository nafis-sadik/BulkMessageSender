from abc import ABC

from Models.ViewModels.RobotModel import RobotsModel
from Repositories.SeliniumRepositories.IBrowserService import IBrowserService
from Services.Abstractions.IRobotOperationsService import IRobotOperationsService


class WhatsappBulkVideoBot(IRobotOperationsService, ABC):
    def __init__(self, browser_service: IBrowserService, robot_model: RobotsModel):
        self.browser_service = browser_service
        self.browser_instance = self.browser_service.get_new_window(
            'https://web.whatsapp.com/',
            robot_model.robot_name,
            robot_model.is_incognito,
            robot_model.is_headless
        )

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def terminate(self):
        self.browser_service.close_window(self.browser_instance)
        self.browser_service = None
