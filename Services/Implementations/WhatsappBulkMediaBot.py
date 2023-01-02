import logging
import os
import platform
from abc import ABC

from selenium.webdriver.common.by import By

from Models.ViewModels.RobotModelVM import RobotsModelVM
from Repositories.SeliniumRepositories.IBrowserService import IBrowserService
from Services.Abstractions.IRobotOperationsService import IRobotOperationsService


class WhatsappBulkVideoBot(IRobotOperationsService, ABC):
    def __init__(self, browser_service: IBrowserService, robot_model: RobotsModelVM):
        self.logger = logging.getLogger('ServerLog')
        self.browser_service = browser_service
        self.execution_flag = True
        self.browser_instance = self.browser_service.get_new_window(
            'https://web.whatsapp.com/',
            robot_model.robot_name,
            robot_model.is_incognito,
            robot_model.is_headless
        )

    def start(self):
        try:
            self.execution_flag = True
            numbers = [1718401788, 1753980951, 1727397219, 1628301510, 1675089000, 1977196627, 4470009942, 1705694207,
                       1713665598, 1715015333, 1774865202]
            while self.execution_flag:
                self.browser_service.open_url_in_browser(browser_instance=self.browser_instance, url='')
                self.browser_service.click_by(self.browser_instance, By.XPATH, os.getenv('WHATSAPP_NEW_CHAT_XPATH'))
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'start'}
            self.logger.error('Whatsapp Bulk Video Bot Service: %s', str(ex), extra=details)

    def stop(self):
        try:
            self.execution_flag = False
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'stop'}
            self.logger.error('Whatsapp Bulk Video Bot Service: %s', str(ex), extra=details)

    def terminate(self):
        try:
            self.browser_service.close_window(self.browser_instance)
            self.browser_service = None
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'terminate'}
            self.logger.error('Whatsapp Bulk Video Bot Service: %s', str(ex), extra=details)
