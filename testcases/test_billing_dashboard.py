import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

from pages.page_billing_dashboard import ResourcesBillingDashboard
from pages.page_onboarding import OnboardingResource
from utilities.readconfig import ReadConfigData
from utilities.XLutils import Excel
from utilities.customlogger import LoggerDemo


@pytest.mark.usefixtures('setup_and_teardown_class')
class TestBillingDashboard:

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.BD = ResourcesBillingDashboard(self.driver)
        self.EX = Excel()

    def test_billing_menu_default_selection(self):
        """Verify Billing menu renders correctly with default selection on Billing Dashboard"""
        # self.PO.wait_until_page_contains_element(self.PO.L_SIGN_UP).click()
        self.BD.login_into_application()
