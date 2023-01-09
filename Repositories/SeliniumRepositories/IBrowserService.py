from selenium import webdriver


class IBrowserService:
    def __init__(self):
        pass

    def get_element(self, browser_instance: webdriver, element_type: str, element_id: str):
        raise NotImplementedError

    def get_elements(self, browser_instance: webdriver, element_type: str, element_id: str):
        raise NotImplementedError

    def get_new_window(self, url: str, user_name: str, use_incognito: bool, use_headless: bool):
        raise NotImplementedError

    def open_url_in_browser(self, url: str, browser_instance: webdriver):
        raise NotImplementedError

    def switch_to_tab(self, browser_instance: webdriver, tab_index: int):
        raise NotImplementedError

    def set_input_value(self, browser_instance: webdriver, element_type: str, element_id: str, element_value: str) -> [None]:
        raise NotImplementedError

    def click_date_on_date_picker(self, browser_instance: webdriver, xpath: str, date: int, element_type: str):
        raise NotImplementedError

    def click_by(self, browser_instance: webdriver, element_type: str, element_id: str) -> [None]:
        raise NotImplementedError

    def upload_file(self, browser_instance: webdriver, element_type: str, element_id: str, file_path: str) -> [None]:
        raise NotImplementedError

    def get_screenshot_by_element(self, browser_instance: webdriver, file_path: str, element_type: str, element_id: str, crop_x: int, crop_y: int):
        raise NotImplementedError

    def set_select_value(self, browser_instance: webdriver, element_type: str, element_id: str, visible_text: str) -> [None]:
        raise NotImplementedError

    def hover_by(self, browser_instance: webdriver, element_type: str, element_id: str) -> [None]:
        raise NotImplementedError

    def scroll_horizontal(self, browser_instance: webdriver, element_type: str, element_id: str, pixels: int):
        raise NotImplementedError

    def scroll_vertical(self, browser_instance: webdriver, y_cord: int):
        raise NotImplementedError

    def refresh_page(self, browser_instance: webdriver):
        raise NotImplementedError

    def get_screenshot(self, browser_instance: webdriver, file_path: str):
        raise NotImplementedError

    def crop_image_by_cords(self, file_path: str, crop_x: int, crop_y: int, origin_x: int, origin_y: int):
        raise NotImplementedError

    def crop_image_by_element(self, browser_instance: webdriver, file_path: str, element_type: str,
                              element_id: str, crop_x: int, crop_y: int):
        raise NotImplementedError

    def alert_response(self, browser_instance: webdriver, response: bool):
        raise NotImplementedError

    def close_window(self, browser_instance: webdriver):
        raise NotImplementedError
