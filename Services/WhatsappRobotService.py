import time

from selenium.webdriver.chrome import webdriver

from Repositories.SeliniumRepositories.IBrowserService import IBrowserService


class WhatsappRobotService:
    def __init__(self, browser_service: IBrowserService, user_name: str):
        self.browser_service = browser_service
        self.browser_driver: webdriver = None
        self.user_name = user_name

    def new_window(self):
        self.browser_driver = self.browser_service.get_new_window('https://www.web.whatsapp.com', self.user_name)
        time.sleep(2000)
        return
