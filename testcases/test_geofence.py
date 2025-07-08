import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

from pages.page_billing_dashboard import ResourcesBillingDashboard
from pages.page_geofence import ResourcesGeofence
from pages.page_onboarding import OnboardingResource
from utilities.readconfig import ReadConfigData
from utilities.XLutils import Excel
from utilities.customlogger import LoggerDemo


@pytest.mark.usefixtures('setup_and_teardown_class')
class TestBillingDashboard:

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.GF = ResourcesGeofence(self.driver)
        self.EX = Excel()

    def test_navigate_to_geofence_module(self):
        """Verify Geofence Module Navigation"""
        self.GF.login_into_application()
        self.GF.navigate_to_geofence_module()
        url_end_point = self.EX.read_data("Common_Data" , "B2")
        self.GF.verify_url_contains(url_end_point)
        print(url_end_point)

