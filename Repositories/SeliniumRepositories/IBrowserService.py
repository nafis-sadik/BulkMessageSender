import string

from selenium import webdriver


class IBrowserService:
    def __init__(self):
        pass

    def get_elements(self, browser_instance: webdriver, element_type: string, element_id: string):
        raise NotImplementedError

    def get_new_window(self, url: string, user_name: string, use_incognito: bool, use_headless: bool):
        raise NotImplementedError

    def switch_to_tab(self, browser_instance: webdriver, tab_index: int):
        raise NotImplementedError

    def set_input_value(self, browser_instance: webdriver, element_type: string, element_id: string, element_value: string) -> [None]:
        raise NotImplementedError

    def click_date_on_date_picker(self, browser_instance: webdriver, xpath: string, date: int, element_type: string):
        raise NotImplementedError

    def click_by(self, browser_instance: webdriver, element_type: string, element_id: string) -> [None]:
        raise NotImplementedError

    def get_screenshot_by_element(self, browser_instance: webdriver, file_path: string, element_type: string, element_id: string, crop_x: int, crop_y: int):
        raise NotImplementedError

    def set_select_value(self, browser_instance: webdriver, element_type: string, element_id: string, visible_text: string) -> [None]:
        raise NotImplementedError

    def hover_by(self, browser_instance: webdriver, element_type: string, element_id: string) -> [None]:
        raise NotImplementedError

    def scroll_horizontal(self, browser_instance: webdriver, element_type: string, element_id: string, pixels: int):
        raise NotImplementedError

    def scroll_vertical(self, browser_instance: webdriver, y_cord: int):
        raise NotImplementedError

    def refresh_page(self, browser_instance: webdriver):
        raise NotImplementedError

    def get_screenshot(self, browser_instance: webdriver, file_path: string):
        raise NotImplementedError

    def crop_image_by_cords(self, file_path: string, crop_x: int, crop_y: int, origin_x: int, origin_y: int):
        raise NotImplementedError

    def crop_image_by_element(self, browser_instance: webdriver, file_path: string, element_type: string,
                              element_id: string, crop_x: int, crop_y: int):
        raise NotImplementedError

    def close_window(self, browser_instance: webdriver):
        raise NotImplementedError