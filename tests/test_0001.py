import time, os, sys

import pytest

from lib import logger
from lib.test_service import TestService
from screens import screen
from screens.general import General
from screens.home import Home
from screens.login import Login
import conftest

class Test:
    # Test parameters:
    platform = None
    driver = None
    testNum     = "0001"
    status      = "Pass"
    
    # Test services
    testService = TestService()
    
    # Get supported platforms for this test - Android, IOS
    supported_platforms = testService.updatePlatforms(testNum)
    
    # Test Setup
    @pytest.fixture(scope='module',params=supported_platforms)
    def setup(self, request):
        logger.info('Test Setup Start')
        global platform, driver
        # Get platform from the platform list (testSet.csv)
        platform = request.param
        # Return WebDriver (android/ios)
        driver = self.testService.setup(platform)
        logger.info('Test Setup End')
        
    # Test Flow        
    def test_0001(self, setup):
        try:
            # Capture test start time
            self.startTime = time.time()
            logger.info('Test Flow Start')
            # Tested Screens
            home = Home(platform, driver) 
            login = Login(platform, driver)
            general = General(platform, driver)
            
            # Steps:
            home.click_user_image_view()
            login.click_login_button()
            login.type_login_username('admin')
            login.type_login_password('123456')
            general.hide_keyboard()
            login.click_signin_button()
            time.sleep(5)
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = self.testService.handleException(self, inst, self.startTime)        
    
    #Test TearDown
    def teardown_method(self, method):
        # Take last screenshot before quitting
        driver.save_screenshot(conftest.LSAT_SCREENSHOT_PATH)    
        driver.quit()
        #write to log we finished the test
        logger.info(self.startTime)
        assert(self.status == "Pass") 
        
    if __name__ == "__main__":  
        pytest.main('test_' + testNum  + '.py -s --tb=line')