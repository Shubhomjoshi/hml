import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_google_search(driver):
    driver.get("https://www.google.com/")
    assert "Google" in driver.title
    TB_search_box = driver.find_element("name", "q")
    TB_search_box.send_keys("Selenium Python")
    TB_search_box.submit()
    time.sleep(2)
    # allure.attach(driver.get_screenshot_as_png(), name="google", attachment_type=AttachmentType.PNG)
    assert "Selenium Pytho1n" in driver.title