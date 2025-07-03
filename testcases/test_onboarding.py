import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
from pages.page_onboarding import OnboardingResource
from utilities.readconfig import ReadConfigData
from utilities.XLutils import Excel
from utilities.customlogger import LoggerDemo


@pytest.mark.usefixtures('setup_and_teardown_class')
class TestSurvey:

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.PO = OnboardingResource(self.driver)
        self.EX = Excel()

    def test_vl_1(self):
        """VL-01 Verify UI of introduction page"""
        self.PO.wait_until_page_contains_element(self.PO.L_SIGN_UP).click()
        time.sleep(1)
