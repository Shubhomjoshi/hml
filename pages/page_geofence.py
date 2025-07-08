from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from base.base_driver import BaseDriver
from selenium.webdriver.common.keys import Keys


class ResourcesGeofence(BaseDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    L_SIGN_UP = By.XPATH, "//span[contains(tex(), 'Sign Up')]"
    L_MENU_GEOFENCE = (By.XPATH, "//ul[@class='main-menu']/li/a[@href='/geofence']")
    # Functions from here
    def nav_to_survey(self):
        self.wait_until_page_contains_element(self.L_SIGN_UP)

    def navigate_to_geofence_module(self):
        self.wait_until_page_contains_element(self.L_MENU_GEOFENCE).click()

