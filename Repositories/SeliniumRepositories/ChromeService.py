import getpass
import os
import platform
import time
from abc import ABC

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from Repositories.SeliniumRepositories.IBrowserService import IBrowserService


class ChromeService(IBrowserService, ABC):
    def __init__(self):
        super().__init__()
        self.__time_wait_limit: int = 10
        self.pid: int = 0

    def get_element(self, browser_instance: webdriver, element_type: str, element_id: str):
        try:
            browser_instance.implicitly_wait(200)

            resource = browser_instance.find_element(element_type, element_id)
            # resource = WebDriverWait(
            #     driver=browser_instance,
            #     timeout=self.__time_wait_limit,
            #     poll_frequency=1) \
            #     .until(ec.visibility_of_element_located((element_type, element_id)))

            return resource
        except Exception as e:
            print(str(e))
            return None

    def get_elements(self, browser_instance: webdriver, element_type: str, element_id: str):
        try:
            resource = WebDriverWait(
                driver=browser_instance,
                timeout=self.__time_wait_limit,
                poll_frequency=1) \
                .until(ec.visibility_of_all_elements_located((element_type, element_id)))

            return resource
        except Exception as e:
            print(str(e))
            return None
        # .until(ec.presence_of_all_elements_located((element_type, element_id)))

    def get_new_window(self, url: str, user_name: str, use_incognito: bool, use_headless: bool):
        # Resolve platform dependency
        system_platform = platform.system()
        pc_user_name = getpass.getuser()

        # Configure browser
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1280,720")
        options.add_argument("--start-maximized")
        if use_incognito:
            options.add_argument("--incognito")
        if use_headless:
            options.add_argument("--headless")  # enable headless mode
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--disable—gpu')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        dir_path = os.path.dirname(os.path.join(__file__))
        print(dir_path)
        # Windows driver path
        if system_platform == 'Windows':
            # Path to your chrome profile
            options.add_argument(
                'user-data-dir=C:\\Users\\' + pc_user_name + '\\AppData\\Local\\Google\\Chrome\\User'
            )
            driver_path = dir_path + '/chromedriver.exe'
        elif system_platform == 'Linux':
            options.add_argument('--user-data-dir=/home/' + pc_user_name + '/.config/google-chrome/' + user_name)
            driver_path = 'chromedriver'  # linux driver path
        else:
            raise PermissionError

        browser_instance: webdriver = webdriver.Chrome(executable_path=driver_path, options=options)
        browser_instance.implicitly_wait(self.__time_wait_limit)
        browser_instance.get(url)
        self.pid = browser_instance.service.process.pid
        print(self.pid)
        return browser_instance

    def open_url_in_browser(self, url: str, browser_instance: webdriver):
        browser_instance.get(url)

    def click_by(self, browser_instance: webdriver, element_type: str, element_id: str):
        browser_instance.implicitly_wait(200)
        element = self.get_element(browser_instance, element_type, element_id)
        if element is not None:
            element.click()

    def upload_file(self, browser_instance: webdriver, element_type: str, element_id: str, file_path: str) -> [None]:
        browser_instance.implicitly_wait(200)
        element = self.get_element(browser_instance, element_type, element_id)
        if element is not None:
            element.send_keys(file_path)

    def hover_by(self, browser_instance: webdriver, element_type: str, element_id: str):
        browser_instance.implicitly_wait(200)
        element = self.get_element(browser_instance, element_type, element_id)
        if element is not None:
            ActionChains(browser_instance).move_to_element(element).perform()
        else:
            print('Chrome Service :: hover_by :: Element not found')
            return None

    def set_input_value(self, browser_instance: webdriver, element_type: str, element_id: str, input_value: str):
        browser_instance.implicitly_wait(200)
        element = self.get_element(browser_instance, element_type, element_id)
        if element is not None:
            element.clear()
            element.send_keys(input_value)
        else:
            print('Chrome Service :: set_select_value :: Element not found')
            print(element_type, element_id, input_value)

    def set_select_value(self, browser_instance: webdriver, element_type: str, element_id: str, visible_text: str):
        browser_instance.implicitly_wait(200)
        element = self.get_element(browser_instance, element_type, element_id)
        if element is not None:
            select = Select(element)
            select.select_by_visible_text(visible_text)
        else:
            print('Chrome Service :: set_select_value :: Element not found')
            print(element_type, element_id, visible_text)

    def click_date_on_date_picker(self, browser_instance: webdriver, element_id: str, date: int,
                                  element_type: str = By.XPATH):
        try:
            calender = self.get_elements(
                browser_instance=browser_instance,
                element_type=element_type,
                element_id=element_id
            )
            calender[date - 1].click()
            return browser_instance
        except Exception as e:
            print(str(e))

    # XPath is not supported yet, we are using jquery for now.
    def scroll_horizontal(self, browser_instance: webdriver, element_type: str, element_id: str, pixels: int):
        try:
            if element_type == By.ID:
                jquery_param = '#' + element_id
            elif element_type == By.CLASS_NAME:
                jquery_param = '.' + element_id
            elif element_type == By.TAG_NAME:
                jquery_param = element_id
            else:
                print('Unsupported element identifier')
                raise Exception

            jquery_script = "$('" + jquery_param + "').scrollLeft(" + str(pixels) + ");"
            browser_instance.execute_script(jquery_script)
            return browser_instance
        except Exception as e:
            print(str(e))

    def scroll_vertical(self, browser_instance: webdriver, y_cord: int):
        try:
            js_script = 'window.scroll(0,' + str(y_cord) + ')'
            browser_instance.execute_script(js_script)
            return browser_instance
        except Exception as e:
            print(str(e))

    def refresh_page(self, browser_instance: webdriver):
        try:
            browser_instance.refresh()
        except Exception as e:
            print(str(e))

    def get_screenshot(self, browser_instance: webdriver, file_path: str):
        try:
            browser_instance.implicitly_wait(500)
            browser_instance.save_screenshot(file_path)
            return file_path
        except Exception as e:
            print(str(e))

    def get_screenshot_by_element(self,
                                  browser_instance: webdriver,
                                  file_path: str,
                                  element_type: str,
                                  element_id: str,
                                  crop_x: int, crop_y: int
                                  ):
        try:
            time.sleep(2)
            element = self.get_element(browser_instance, element_type, element_id)
            if element is not None:
                element.screenshot(file_path)
            else:
                print('Chrome Service :: set_select_value :: Element not found')
                print(element_type, element_id, file_path)
        except Exception as e:
            print(str(e))

    def crop_image_by_element(self,
                              browser_instance: webdriver,
                              file_path: str,
                              element_type: str,
                              element_id: str,
                              crop_x: int, crop_y: int
                              ):
        try:
            element = self.get_element(browser_instance, element_type, element_id)
            if element is None:
                print('Chrome Service :: set_select_value :: Element not found')
                print(element_type, element_id, file_path)
                raise Exception(f'element {element_id} of type {element_type} was not found')
            location = element.location
            image = Image.open(file_path)
            location_x, location_y = location['x'], location['y']
            image.crop((location_x, location_y, location_x + crop_x, location_y + crop_y)).save(file_path)
            return file_path
        except Exception as e:
            print(str(e))

    def crop_image_by_cords(self, file_path: str, crop_x: int, crop_y: int, origin_x: int, origin_y: int):
        try:
            location = {
                'x': origin_x,
                'y': origin_y
            }
            image = Image.open(file_path)
            location_x, location_y = location['x'], location['y']
            image.crop((location_x, location_y, location_x + crop_x, location_y + crop_y)).save(file_path)
            return file_path
        except Exception as e:
            print(e)

    def alert_response(self, browser_instance: webdriver, response: bool):
        if response is True:
            browser_instance.switch_to.alert.accept()
        else:
            browser_instance.switch_to.alert.dismiss()

    def close_window(self, browser_instance: webdriver):
        try:
            time.sleep(self.__time_wait_limit / 2)
            browser_instance.quit()
        except Exception as e:
            print(str(e))
