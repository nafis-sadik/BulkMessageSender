import logging
import os
import platform
import time
from abc import ABC

from selenium.webdriver.common.by import By

from Models.Entities.Entity import Contacts, CampaignHistory
from Models.ViewModels.RobotModelVM import RobotsModelVM
from Repositories.DbRepositories.IRepositoryBase import IRepositoryBase
from Repositories.DbRepositories.RepositoryBase import RepositoryBase
from Repositories.SeliniumRepositories.IBrowserService import IBrowserService
from Services.Abstractions.IRobotOperationsService import IRobotOperationsService


class WhatsappBulkVideoBot(IRobotOperationsService, ABC):
    def __init__(self, browser_service: IBrowserService, robot_model: RobotsModelVM):
        self.logger = logging.getLogger('ServerLog')
        self.contact_repo: IRepositoryBase = RepositoryBase(Contacts)
        self.campaign_history_repo: IRepositoryBase = RepositoryBase(CampaignHistory)
        self.browser_service = browser_service
        self.execution_flag = True
        self.browser_instance = self.browser_service.get_new_window(
            'https://web.whatsapp.com/',
            robot_model.robot_name,
            robot_model.is_incognito,
            robot_model.is_headless
        )

    async def start(self):
        try:
            self.execution_flag = True
            while self.execution_flag:
                contact_data: Contacts = await self.contact_repo.get(Contacts.booking_status != True)
                if contact_data is None:
                    self.execution_flag = False
                    continue
                contact_data.booking_status = True
                print(contact_data.contact_number)
                await self.contact_repo.commit()

                self.browser_service.open_url_in_browser(
                    browser_instance=self.browser_instance,
                    url='https://web.whatsapp.com/send/?phone='
                        + str(contact_data.contact_number)
                        + '&text&type=phone_number&app_absent=0%22'
                )

                # Number does not exist popup
                print('Checking modal_ui update')
                modal_ui = self.browser_service.get_element(
                    self.browser_instance,
                    By.XPATH,
                    os.getenv('NUMBER_NOT_FOUND_POPUP')
                )
                print('modal_ui update received')

                time.sleep(2)

                if modal_ui is None:
                    print('Modal UI doesnt exist')
                    continue

                try:
                    if 'Phone number shared via url is invalid.' == modal_ui.text:
                        print('Number doesnt exist')
                        print(modal_ui.text)
                        continue
                except Exception as ex:
                    details = {'platform': platform.node(), 'target': 'start > modal_ui'}
                    self.logger.error('Whatsapp Bulk Video Bot Service: %s', str(ex), extra=details)

                print('modal_ui update validated')
                # Click attachment button
                self.browser_service.click_by(self.browser_instance, By.XPATH, os.getenv('ATTACHMENT_BUTTON_XPATH'))
                print('Attachment button clicked')

                # Click Picture/Video button
                self.browser_service.click_by(self.browser_instance, By.XPATH, os.getenv('MEDIA_BUTTON_XPATH'))
                print('Media button clicked')

                # Upload File
                self.browser_service.upload_file(
                    browser_instance=self.browser_instance,
                    element_type=By.XPATH,
                    element_id=os.getenv('MEDIA_INPUT_FIELD_XPATH_FULL'),
                    file_path="C:/Users/nafis/Downloads/videoplayback.mp4"
                )
                print('File upload input field filled')
                time.sleep(3)

                # Click Send button
                self.browser_service.click_by(self.browser_instance, By.XPATH, os.getenv('SEND_BUTTON_DIRECT_XPATH'))
                print('Send button clicked')
                time.sleep(3)
            await self.contact_repo.close()
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
