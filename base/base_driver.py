from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
from utilities.readconfig import ReadConfigData


class BaseDriver:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)

    config = ReadConfigData()

    B_MICROSOFT = By.XPATH, "//button"
    TB_EMAIL = By.XPATH, "//input[@name='loginfmt']"
    B_NEXT = By.XPATH, "//input[@value='Next']"
    TB_PASSWORD = By.XPATH, "//input[@name='passwd']"
    B_SIGN_IN = By.XPATH, "//input[@value='Sign in']"
    B_NO = By.XPATH, "//input[@value='No']"
    IMG_MAIN_LOGO = By.XPATH, "//img[@class='desktop-dark']"
    T_EPM_DASHBOARD = By.XPATH, "//h5[contains(text(), 'Dashboard')]"

    def login_into_application(self):
        """Log into connect app and wait till logo appear"""
        self.wait_until_page_contains_element(self.B_MICROSOFT).click()
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        config = ReadConfigData()
        Email = config.get_config_data('Credentials', 'Email')
        self.fill_single_data_in_textboxes(self.TB_EMAIL, Email)
        self.wait_until_page_contains_element(self.B_NEXT).click()
        Password = config.get_config_data('Credentials', 'Password')
        self.wait_until_element_is_clickable(self.TB_PASSWORD)
        self.fill_single_data_in_textboxes(self.TB_PASSWORD, Password)
        self.wait_until_page_contains_element(self.B_SIGN_IN).click()
        self.wait_until_page_contains_element(self.B_NO).click()
        self.driver.switch_to.window(handles[0])
        # self.wait_for_page_to_be_ready()
        # self.wait_until_element_is_visible(self.IMG_MAIN_LOGO)
        # time.sleep(40)
        self.verify_single_text(self.T_EPM_DASHBOARD, "Dashboard")

    def wait_for_page_to_be_ready(self, timeout=30):
        """Waits until the document.readyState is 'complete'."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete')

    def wait_until_page_contains_element(self, locator):
        """Waits until the DOM contains the element"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_until_element_is_visible(self, locator, timeout=30):
        """Waits until the element is visible (not just present in DOM)."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_until_element_is_clickable(self, locator, timeout=30):
        """Waits until the element is visible and enabled (clickable)."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def verify_single_text(self, locator, text):
        """Get text from locator and verify it."""
        Text = self.wait.until(EC.presence_of_element_located(locator)).text
        assert Text == text

    def verify_multiple_labels(self, dictionary):
        """It runs the loop for verify multiple text from dictionary."""
        for key, value in dictionary.items():
            self.verify_single_text(key, value)

    def fill_single_data_in_textboxes(self, locator, text):
        """It is used to add text in textbox at once."""
        self.wait_until_page_contains_element(locator).click()
        self.actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        self.wait_until_page_contains_element(locator).send_keys(text)

    def fill_multiple_data_in_textboxes(self, dictionary):
        """It runs the loop for adding multiple text from dictionary into textbox."""
        for key, value in dictionary.items():
            self.fill_single_data_in_textboxes(key, value)
