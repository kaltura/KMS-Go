import time, os, sys

import pytest

from screens.home import Home
from screens.login import Login
from lib import logger
from lib.test_service import TestService

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
#         return driver
        
    # Test Flow        
    def test_0001(self, setup):
#         global platform
        try:
            # Capture test start time
            self.startTime = time.time()
            logger.info('Test Flow Start')
            # Tested Screens
            home = Home(platform, driver) 
            login = Login(platform, driver)
            
            # Steps:
            home.click_user_image_view()
            login.click_login_button()
            login.type_login_username('admin')
            login.type_login_password('123456')
            # click on the background to hide the
            login.click_coordinates_login_frame(0,0) 
            login.click_signin_button()
            time.sleep(5)
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = self.testService.handleException(self, inst, self.startTime)        
    
    #Test TearDown
    def teardown_method(self, method):
        driver.quit()
        #write to log we finished the test
        logger.info(self.startTime)
        assert(self.status == "Pass") 
        
    if __name__ == "__main__":  
    #     pytest.main('test_0001.py -s')
        pytest.main('test_' + testNum  + '.py -s --tb=line')