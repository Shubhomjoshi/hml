# Setup and Teardown code:
# Mandatory to import
import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver

# Optional to import
import os
from utilities.readconfig import ReadConfigData
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="class")
def setup_and_teardown_class(request):
    browser = request.config.getoption("--browser")
    environment = request.config.getoption("--env")
    if browser == 'chrome':
       # driver = webdriver.Chrome()

        # For running in headless mode
        options = Options()
        if os.getenv("GITHUB_ACTIONS") == "true":
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=options)
        # Ends here

    elif browser == 'firefox':
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Browser {browser} is not supported")
    config = ReadConfigData()
    if environment == 'stage':
        base_url = config.get_config_data('Environment URL', 'Stage')
    elif environment == 'prod':
        base_url = config.get_config_data('Environment URL', 'Prod')
    else:
        raise ValueError(f"Environment '{environment}' is not supported. Use 'stage' or 'prod'.")
    driver.get(base_url)
    driver.maximize_window()

    # Assign driver and self.wait to the request's class
    request.cls.driver = driver

    yield
    # Teardown code: Runs once after all test methods in the class
    driver.quit()  # Ensure the browser is closed properly


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Browser option: Chrome or firefox")
    parser.addoption("--env", default="stage", help="Environment: stage or prod")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This is the hook to get the test report
    outcome = yield
    report = outcome.get_result()

    # We only want to take a screenshot when a test fails during the call phase
    if report.when == "call" and report.failed:
        # Check if the fixture `driver` is used in the test
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            if driver:
                try:
                    screenshot = driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Failure Screenshot", attachment_type=AttachmentType.PNG)
                    print("Screenshot captured and attached to Allure report.")
                except Exception as e:
                    print(f"Failed to capture screenshot: {e}")
