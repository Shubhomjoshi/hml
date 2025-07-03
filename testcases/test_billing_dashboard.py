import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

from hml.pages.page_billing_dashboard import ResourcesBillingDashboard
from hml.pages.page_onboarding import OnboardingResource
from hml.utilities.readconfig import ReadConfigData
from hml.utilities.XLutils import Excel
from hml.utilities.customlogger import LoggerDemo


@pytest.mark.usefixtures('setup_and_teardown_class')
class TestBillingDashboard:

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.BD = ResourcesBillingDashboard(self.driver)
        self.EX = Excel()

    def test_billing_menu_default_selection(self):
        # self.PO.wait_until_page_contains_element(self.PO.L_SIGN_UP).click()
        self.BD.login_into_application()
        time.sleep(1)